import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import { Activity, RefreshCw, Clock, User, FileText, TrendingUp } from 'lucide-react';

const SessionMonitor = ({ adminToken }) => {
  const [activeSessions, setActiveSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);
  const [userSessions, setUserSessions] = useState([]);

  useEffect(() => {
    fetchActiveSessions();
    
    if (autoRefresh) {
      const interval = setInterval(fetchActiveSessions, 5000); // 每5秒刷新
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const fetchActiveSessions = async () => {
    try {
      const response = await axios.get('/api/admin/sessions/active', {
        headers: { Authorization: `Bearer ${adminToken}` }
      });
      setActiveSessions(response.data);
    } catch (error) {
      if (error.response?.status !== 401) {
        console.error('获取活跃会话失败:', error);
      }
    }
  };

  const fetchUserSessions = async (userId, cardKey) => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/admin/users/${userId}/sessions`, {
        headers: { Authorization: `Bearer ${adminToken}` }
      });
      setUserSessions(response.data);
      setSelectedUser({ id: userId, card_key: cardKey });
    } catch (error) {
      toast.error('获取用户会话历史失败');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processing':
        return 'bg-blue-500';
      case 'completed':
        return 'bg-green-500';
      case 'failed':
        return 'bg-red-500';
      case 'queued':
        return 'bg-yellow-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'processing':
        return '处理中';
      case 'completed':
        return '已完成';
      case 'failed':
        return '失败';
      case 'queued':
        return '排队中';
      default:
        return status;
    }
  };

  const formatDuration = (seconds) => {
    if (!seconds) return '-';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}分${secs}秒`;
  };

  return (
    <div className="space-y-6">
      {/* 头部 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Activity className="w-6 h-6 text-purple-600" />
          <h3 className="text-xl font-semibold text-gray-800">会话监控</h3>
        </div>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            自动刷新
          </label>
          <button
            onClick={() => fetchActiveSessions()}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            <RefreshCw className="w-5 h-5" />
            刷新
          </button>
        </div>
      </div>

      {/* 活跃会话统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm">活跃会话</p>
              <p className="text-3xl font-bold mt-1">{activeSessions.length}</p>
            </div>
            <Activity className="w-12 h-12 text-blue-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm">处理中</p>
              <p className="text-3xl font-bold mt-1">
                {activeSessions.filter(s => s.status === 'processing').length}
              </p>
            </div>
            <TrendingUp className="w-12 h-12 text-green-200" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 text-white rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-yellow-100 text-sm">排队中</p>
              <p className="text-3xl font-bold mt-1">
                {activeSessions.filter(s => s.status === 'queued').length}
              </p>
            </div>
            <Clock className="w-12 h-12 text-yellow-200" />
          </div>
        </div>
      </div>

      {/* 活跃会话列表 */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h4 className="text-lg font-semibold text-gray-800 mb-4">实时会话</h4>
        {activeSessions.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            当前没有活跃会话
          </div>
        ) : (
          <div className="space-y-4">
            {activeSessions.map((session) => (
              <div
                key={session.id}
                className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <button
                        onClick={() => fetchUserSessions(session.user_id, session.card_key)}
                        className="flex items-center gap-2 px-3 py-1 bg-purple-100 hover:bg-purple-200 text-purple-800 rounded-lg transition-colors text-sm font-medium"
                      >
                        <User className="w-4 h-4" />
                        {session.card_key}
                      </button>
                      <span className={`px-2 py-1 text-xs font-medium rounded ${
                        session.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                        session.status === 'queued' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {getStatusText(session.status)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {session.original_text?.substring(0, 100)}
                      {session.original_text?.length > 100 ? '...' : ''}
                    </p>
                  </div>
                </div>

                {/* 进度条 */}
                {session.total_segments > 0 && (
                  <div className="mb-3">
                    <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                      <span>处理进度</span>
                      <span>{session.processed_segments}/{session.total_segments} 段</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all duration-300 ${getStatusColor(session.status)}`}
                        style={{
                          width: `${(session.processed_segments / session.total_segments) * 100}%`
                        }}
                      />
                    </div>
                  </div>
                )}

                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {new Date(session.created_at).toLocaleString('zh-CN')}
                  </span>
                  {session.processing_time && (
                    <span>耗时: {formatDuration(session.processing_time)}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 用户会话历史模态框 */}
      {selectedUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <User className="w-6 h-6 text-purple-600" />
                <h3 className="text-xl font-bold text-gray-800">
                  用户会话历史: {selectedUser.card_key}
                </h3>
              </div>
              <button
                onClick={() => setSelectedUser(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <span className="text-2xl">&times;</span>
              </button>
            </div>

            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
              </div>
            ) : userSessions.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                该用户暂无会话记录
              </div>
            ) : (
              <div className="space-y-4">
                {userSessions.map((session) => (
                  <div key={session.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          session.status === 'completed' ? 'bg-green-100 text-green-800' :
                          session.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                          session.status === 'failed' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {getStatusText(session.status)}
                        </span>
                        <span className="text-xs text-gray-500">
                          ID: {session.id}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500">
                        {new Date(session.created_at).toLocaleString('zh-CN')}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-3">
                      <div className="bg-gray-50 rounded-lg p-3">
                        <p className="text-xs text-gray-500 mb-1">原文</p>
                        <p className="text-sm text-gray-700 line-clamp-3">
                          {session.original_text?.substring(0, 100)}
                          {session.original_text?.length > 100 ? '...' : ''}
                        </p>
                      </div>
                      {session.optimized_text && (
                        <div className="bg-gray-50 rounded-lg p-3">
                          <p className="text-xs text-gray-500 mb-1">优化后</p>
                          <p className="text-sm text-gray-700 line-clamp-3">
                            {session.optimized_text.substring(0, 100)}
                            {session.optimized_text.length > 100 ? '...' : ''}
                          </p>
                        </div>
                      )}
                    </div>

                    <div className="flex items-center gap-6 text-xs text-gray-600">
                      <span className="flex items-center gap-1">
                        <FileText className="w-3 h-3" />
                        分段: {session.processed_segments || 0}/{session.total_segments || 0}
                      </span>
                      {session.processing_time && (
                        <span>耗时: {formatDuration(session.processing_time)}</span>
                      )}
                      {session.completed_at && (
                        <span>完成: {new Date(session.completed_at).toLocaleString('zh-CN')}</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SessionMonitor;
