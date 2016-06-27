# coding: utf-8
# Author: Dunkle Qiu
from rest_framework import serializers

from .models import ExUser, ExGroup


class ExUserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField('name', many=True, read_only=True)
    mana_group_set = serializers.SlugRelatedField('name', many=True, read_only=True)

    class Meta:
        model = ExUser
        fields = ('id', 'username', 'name', 'role', 'last_login', 'groups', 'mana_group_set')


class ExGroupSerializer(serializers.ModelSerializer):
    user_set = ExUserSerializer(many=True, read_only=True)
    managers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ExGroup
        fields = ('id', 'name', 'comment', 'member_type', 'user_set', 'managers')
