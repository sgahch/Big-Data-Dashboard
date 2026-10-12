from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Message, MessageTemplate
from .serializers import MessageSerializer, MessageTemplateSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """消息视图集"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Message.objects.filter(receiver=self.request.user)
        is_read = self.request.query_params.get('is_read')
        msg_type = self.request.query_params.get('msg_type')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read == 'true')
        if msg_type:
            queryset = queryset.filter(msg_type=msg_type)
        return queryset

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """获取未读消息数量"""
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return Response({'unread_count': count})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """标记消息为已读"""
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'status': 'ok'})


class MessageTemplateViewSet(viewsets.ModelViewSet):
    """消息模板视图集"""
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated]
