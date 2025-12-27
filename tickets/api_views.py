from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Ticket, Comment, User
from .serializers import (
    TicketSerializer, TicketCreateSerializer, TicketUpdateSerializer,
    CommentSerializer, CommentCreateSerializer
)


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ticket CRUD operations
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin():
            return Ticket.objects.all()
        elif user.is_it_staff():
            return Ticket.objects.filter(
                Q(assigned_to=user) | Q(assigned_to__isnull=True) | Q(created_by=user)
            )
        else:
            return Ticket.objects.filter(created_by=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        return TicketSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        ticket = self.get_object()
        old_status = ticket.status
        serializer.save()
        
        # Handle status change
        ticket.refresh_from_db()
        if old_status != ticket.status:
            ticket.update_status(ticket.status, self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a ticket"""
        ticket = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            comment = serializer.save(
                ticket=ticket,
                author=request.user
            )
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update ticket status"""
        ticket = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Status is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_status not in dict(Ticket.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check permissions
        if not (request.user.is_it_staff() or request.user.is_admin()):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        ticket.update_status(new_status, request.user)
        return Response(TicketSerializer(ticket).data)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign ticket to IT staff"""
        ticket = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check permissions
        if not (request.user.is_it_staff() or request.user.is_admin()):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = get_object_or_404(User, id=user_id)
        if not (user.is_it_staff() or user.is_admin()):
            return Response(
                {'error': 'Can only assign to IT staff or admin'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.assigned_to = user
        ticket.save()
        
        # Create system comment
        Comment.objects.create(
            ticket=ticket,
            author=request.user,
            content=f"Ticket assigned to {user.username}",
            is_system_message=True
        )
        
        return Response(TicketSerializer(ticket).data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment operations
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        ticket_id = self.request.query_params.get('ticket_id')
        if ticket_id:
            return Comment.objects.filter(ticket_id=ticket_id)
        return Comment.objects.all()
    
    def perform_create(self, serializer):
        ticket_id = self.request.data.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id)
        
        # Check permissions
        if not (self.request.user.is_admin() or 
                self.request.user.is_it_staff() or 
                ticket.created_by == self.request.user):
            raise PermissionDenied('You do not have permission to comment on this ticket.')
        
        serializer.save(author=self.request.user, ticket=ticket)

