from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from boards.models import Board
from boards.serializers import BoardSerializer


@api_view(['GET'])
def board_list(request):
    boards = Board.objects.all()
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BoardSerializer(board)
    return Response(serializer.data)
