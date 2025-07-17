import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { topicsAPI, learningPathsAPI } from '../services/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  BookOpen, 
  Brain, 
  Video, 
  Plus, 
  TrendingUp,
  Clock,
  Target,
  Sparkles
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    topics: 0,
    learningPaths: 0,
    videos: 0,
    completedLessons: 0
  });
  const [recentTopics, setRecentTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const topicsResponse = await topicsAPI.getTopics();
        const topics = topicsResponse.data;
        setRecentTopics(topics.slice(0, 3));
        
        // Calculate stats
        let totalPaths = 0;
        for (const topic of topics) {
          try {
            const pathsResponse = await learningPathsAPI.getLearningPaths(topic.id);
            totalPaths += pathsResponse.data.length;
          } catch (error) {
            console.error('Error fetching learning paths:', error);
          }
        }
        
        setStats({
          topics: topics.length,
          learningPaths: totalPaths,
          videos: 0, // Will be calculated when videos are implemented
          completedLessons: 0 // Will be calculated when progress tracking is implemented
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const quickActions = [
    {
      title: 'Create New Topic',
      description: 'Start a new learning journey',
      icon: BookOpen,
      href: '/topics/new',
      color: 'bg-blue-500'
    },
    {
      title: 'Generate Learning Path',
      description: 'AI-powered curriculum creation',
      icon: Brain,
      href: '/learning-paths/new',
      color: 'bg-purple-500'
    },
    {
      title: 'Create Video',
      description: 'Generate narrated lessons',
      icon: Video,
      href: '/videos/new',
      color: 'bg-green-500'
    }
  ];

  const statCards = [
    {
      title: 'Topics',
      value: stats.topics,
      icon: BookOpen,
      description: 'Learning subjects',
      color: 'text-blue-600'
    },
    {
      title: 'Learning Paths',
      value: stats.learningPaths,
      icon: Brain,
      description: 'Structured curricula',
      color: 'text-purple-600'
    },
    {
      title: 'Videos Generated',
      value: stats.videos,
      icon: Video,
      description: 'AI-narrated lessons',
      color: 'text-green-600'
    },
    {
      title: 'Lessons Completed',
      value: stats.completedLessons,
      icon: Target,
      description: 'Learning progress',
      color: 'text-orange-600'
    }
  ];

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-muted rounded w-1/3"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-muted rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">
            Welcome back, {user?.full_name || user?.email?.split('@')[0]}!
          </h1>
          <p className="text-muted-foreground mt-1">
            Continue your AI-powered learning journey
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Button asChild>
            <Link to="/topics/new">
              <Plus className="h-4 w-4 mr-2" />
              New Topic
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">
                      {stat.title}
                    </p>
                    <p className="text-2xl font-bold text-foreground">
                      {stat.value}
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {stat.description}
                    </p>
                  </div>
                  <Icon className={`h-8 w-8 ${stat.color}`} />
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-foreground mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <Card key={action.title} className="hover:shadow-md transition-shadow cursor-pointer">
                <Link to={action.href}>
                  <CardContent className="p-6">
                    <div className="flex items-center space-x-4">
                      <div className={`p-3 rounded-lg ${action.color}`}>
                        <Icon className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-foreground">{action.title}</h3>
                        <p className="text-sm text-muted-foreground">{action.description}</p>
                      </div>
                    </div>
                  </CardContent>
                </Link>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Recent Topics */}
      {recentTopics.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-foreground">Recent Topics</h2>
            <Button variant="outline" asChild>
              <Link to="/topics">View All</Link>
            </Button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentTopics.map((topic) => (
              <Card key={topic.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{topic.title}</CardTitle>
                    <Badge variant="secondary">
                      <Clock className="h-3 w-3 mr-1" />
                      {new Date(topic.created_at).toLocaleDateString()}
                    </Badge>
                  </div>
                  {topic.description && (
                    <CardDescription className="line-clamp-2">
                      {topic.description}
                    </CardDescription>
                  )}
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <Button variant="outline" size="sm" asChild>
                      <Link to={`/topics/${topic.id}`}>View Details</Link>
                    </Button>
                    <div className="flex items-center text-sm text-muted-foreground">
                      <TrendingUp className="h-4 w-4 mr-1" />
                      Active
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Getting Started */}
      {stats.topics === 0 && (
        <Card className="border-dashed border-2">
          <CardContent className="p-8 text-center">
            <Sparkles className="h-12 w-12 text-primary mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-foreground mb-2">
              Welcome to Lexora!
            </h3>
            <p className="text-muted-foreground mb-6">
              Get started by creating your first learning topic. Our AI will help you build
              a structured learning path with personalized video lessons.
            </p>
            <Button asChild>
              <Link to="/topics/new">
                <Plus className="h-4 w-4 mr-2" />
                Create Your First Topic
              </Link>
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Dashboard;

