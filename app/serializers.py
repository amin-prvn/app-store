from rest_framework import serializers

from .models import App, Purchase


class AppSerializer(serializers.ModelSerializer):
    # TODO It is better to prevent using ModelSerializer in production
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )
    class Meta:
        model = App
        fields = ['id', 'title', 'icon', 'description', 'owner', 'price']
        read_only_fields = ['owner']
        

class AppOwnerSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )
    class Meta:
        model = App
        fields = ['id', 'title', 'icon', 'description', 'is_verified', 'price', 'link', 'key', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at', 'is_verified']


class PurchaseSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    app = AppSerializer(read_only=True)
    class Meta:
        model = Purchase
        fields = ['id', 'owner', 'app', 'link', 'key', 'price', 'purchase_date']
        read_only_fields = fields

    def create(self, validated_data):
        # TODO We can get or genrate key here
        purchase = Purchase.objects.create(
            link=validated_data['app'].link,
            key=validated_data['app'].key,
            price=validated_data['app'].price,
            **validated_data
            )
        return purchase