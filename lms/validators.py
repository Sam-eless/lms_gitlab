from rest_framework import serializers


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if "youtube.com" not in value.get("url"):
            print(value.get("url"))
            raise serializers.ValidationError("Not youtube url in this video")
