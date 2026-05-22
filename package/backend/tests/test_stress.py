"""
暴力压力测试 — 直接测试 ConcurrencyManager，不依赖超时
"""
import asyncio
import pytest

from app.services.concurrency import ConcurrencyManager


async def _acquire_no_wait(mgr, session_id, user_id=None):
    """acquire 但不等待排队（如果没拿到就算 False）"""
    async with mgr._condition:
        if session_id in mgr.active_sessions:
            return True

        user_count = mgr.active_per_user.get(user_id, 0) if user_id is not None else 0
        can_acquire = (
            len(mgr.active_sessions) < mgr.max_concurrent
            and (user_id is None or user_count < mgr.max_per_user)
        )

        if can_acquire:
            mgr.active_sessions[session_id] = __import__('datetime').datetime.utcnow()
            if user_id is not None:
                mgr.active_per_user[user_id] = mgr.active_per_user.get(user_id, 0) + 1
                mgr._session_user[session_id] = user_id
            return True

        # 加到队列但不等待
        if session_id not in mgr.queue:
            mgr.queue.append(session_id)
            if user_id is not None:
                mgr._session_user[session_id] = user_id
        return False


@pytest.fixture
def mgr():
    m = ConcurrencyManager(max_concurrent=5)
    m.max_per_user = 1
    return m


class TestStressConcurrency:

    def test_first_acquires_second_queues(self, mgr):
        """第1个获取, 第2个排队"""
        async def run():
            r1 = await _acquire_no_wait(mgr, "s1", user_id=42)
            assert r1 == True, "First should acquire immediately"

            r2 = await _acquire_no_wait(mgr, "s2", user_id=42)
            assert r2 == False, "Second should queue"
            assert mgr.get_active_count() == 1
            assert len(mgr.queue) == 1
            assert mgr.active_per_user.get(42) == 1
        asyncio.run(run())

    def test_release_activates_queued_same_user(self, mgr):
        """释放后排队中的同用户任务被激活"""
        async def run():
            await _acquire_no_wait(mgr, "s1", user_id=42)
            await _acquire_no_wait(mgr, "s2", user_id=42)
            assert len(mgr.queue) == 1

            await mgr.release("s1")
            assert mgr.get_active_count() == 1
            assert len(mgr.queue) == 0
            assert mgr.active_per_user.get(42) == 1
        asyncio.run(run())

    def test_two_users_each_get_one_slot(self, mgr):
        """两个用户各自获取一个槽位"""
        async def run():
            r1 = await _acquire_no_wait(mgr, "a1", user_id=1)
            r2 = await _acquire_no_wait(mgr, "b1", user_id=2)
            assert r1 and r2, "Both should acquire"
            assert mgr.get_active_count() == 2
            assert mgr.active_per_user.get(1) == 1
            assert mgr.active_per_user.get(2) == 1
        asyncio.run(run())

    def test_three_different_users(self, mgr):
        """3个不同用户, per_user=1, 各1个槽位, 共3个活跃"""
        async def run():
            for i in range(3):
                r = await _acquire_no_wait(mgr, f"s{i}", user_id=i)
                assert r == True, f"User {i} should acquire"
            assert mgr.get_active_count() == 3
            assert len(mgr.queue) == 0
        asyncio.run(run())

    def test_release_activates_queued_under_per_user_limit(self, mgr):
        """per_user=2时释放, 排队中的同用户被激活"""
        async def run():
            mgr.max_per_user = 2
            await _acquire_no_wait(mgr, "s1", user_id=42)
            await _acquire_no_wait(mgr, "s2", user_id=42)
            r3 = await _acquire_no_wait(mgr, "s3", user_id=42)
            assert r3 == False  # queued
            assert mgr.get_active_count() == 2

            await mgr.release("s1")
            assert mgr.get_active_count() == 2
            assert mgr.active_per_user.get(42) == 2
            assert len(mgr.queue) == 0
        asyncio.run(run())

    def test_release_blocks_if_same_user_at_limit(self, mgr):
        """per_user=1时释放一个, 排队中同用户不应被激活（FIFO排队顺序）"""
        async def run():
            await _acquire_no_wait(mgr, "a1", user_id=1)
            await _acquire_no_wait(mgr, "b1", user_id=2)
            await _acquire_no_wait(mgr, "a2", user_id=1)  # queued (per_user[1]=1)
            await _acquire_no_wait(mgr, "b2", user_id=2)  # queued (per_user[2]=1)

            assert mgr.get_active_count() == 2  # a1 + b1
            assert len(mgr.queue) == 2  # [a2 (user1满), b2 (user2)]

            # 释放 b1 → _activate 检查 a2(user=1) → per_user=1 >= 1 → break (FIFO)
            # a2 排在 b2 前面, 必须等用户1释放槽位后先处理 a2
            await mgr.release("b1")
            assert mgr.get_active_count() == 1  # 只有 a1 (b1 释放后 a2 不能激活, b2 被挡住)
            assert len(mgr.queue) == 2  # a2, b2 都还在排队
        asyncio.run(run())

    def test_high_frequency_no_leak(self, mgr):
        """高频acquire/release 100x, 无泄漏"""
        async def run():
            for _ in range(100):
                assert await _acquire_no_wait(mgr, "s", user_id=1)
                await mgr.release("s")
            assert mgr.get_active_count() == 0
            assert mgr.active_per_user.get(1, 0) == 0
        asyncio.run(run())

    def test_max_concurrent_global_limit(self, mgr):
        """max_concurrent=5, 10个不同用户, 仅5个能获取"""
        async def run():
            acquired = 0
            for i in range(10):
                r = await _acquire_no_wait(mgr, f"s{i}", user_id=i)
                if r:
                    acquired += 1
            assert acquired == 5, f"Expected 5 acquired, got {acquired}"
            assert mgr.get_active_count() == 5
            assert len(mgr.queue) == 5
        asyncio.run(run())

    def test_update_per_user_limit_at_runtime(self, mgr):
        """运行时修改 per_user 限制"""
        async def run():
            mgr.max_per_user = 3
            await _acquire_no_wait(mgr, "s1", user_id=1)
            await _acquire_no_wait(mgr, "s2", user_id=1)
            await _acquire_no_wait(mgr, "s3", user_id=1)
            await _acquire_no_wait(mgr, "s4", user_id=1)  # queued
            assert mgr.get_active_count() == 3

            mgr.max_per_user = 1
            assert mgr.get_active_count() == 3  # 活跃不受影响
            await mgr.release("s1")
            # s4 不应被激活
            assert mgr.get_active_count() == 2
            assert mgr.active_per_user.get(1) == 2
        asyncio.run(run())
