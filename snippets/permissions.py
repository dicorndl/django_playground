from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자만 수정 가능하도록 하는 커스텀 권한
    """

    def has_object_permission(self, request, view, obj):
        # 모든 request 에 대해 읽기 권한은 허락한다.
        # GET, HEAD, OPTIONS request 는 항상 허락.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 snippet 소유자에게만 허락한다.
        return obj.owner == request.user
