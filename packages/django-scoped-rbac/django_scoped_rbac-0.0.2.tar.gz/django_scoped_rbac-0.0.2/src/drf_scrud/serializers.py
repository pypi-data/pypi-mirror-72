from django.db.models import Manager
from django.db.models.query import QuerySet
from rest_framework import serializers


class EnvelopeItemSerializer:
    """Items that will be serialized in an envelope **MUST** be serialized by a class
    that satisfies this interface.
    """

    def etag(self):
        """Return the etag for the resource ``self.instance``"""
        return self.etag_for(self.instance)

    def last_modified(self):
        """Return the last modified value for the resource ``self.instance``"""
        return self.last_modified_for(self.instance)

    def absolute_url_for(self, item):
        """Given an instance of the item to be serialized return its absolute url for
        inclusion in the envelope's properties.
        """
        raise NotImplementedError()

    def link_header_content(self):
        if not hasattr(self, "__link_header__"):
            separator = ""
            if self.schema_url() and self.ld_context_url():
                separator = ", "
            else:
                separator = ""

            if self.schema_url():
                schema_link = f"<{self.schema_url()}>; rel=\"schema\""
            else:
                schema_link = ""

            if self.ld_context_url():
                context_link = f"<{self.ld_context_url()}>; rel=\"http://www.w3.org/ns/json-ld#context\""
            else:
                context_link = ""

            setattr(self, "__link_header__", schema_link + separator + context_link)

        return self.__link_header__

    @classmethod
    def etag_for(cls, item=None, *args, pk=None, **kwargs):
        """Given the primary key ``pk`` or the instance ``item`` to be serialized return
        an etag for the indiciated resource.
        """
        raise NotImplementedError()

    @classmethod
    def last_modified_for(cls, item=None, *args, pk=None, **kwargs):
        """Given the primary key ``pk`` or the instance ``item`` to be serialized return
        the datetime of the last modification made to the indicated resource.
        """
        raise NotImplementedError()

    @classmethod
    def schema_url(self):
        """Return the JSON Schema URL for the resource serialized by this class.
        """
        return None

    @classmethod
    def ld_context_url(self):
        """Return the Linked Data Context URL for the resource serialized by this class.
        """
        return None


class EnvelopeCollectionSerializer(serializers.ListSerializer):
    """Serialize items in a list wrapped in an envelope containing caching headers and
    other properties. The child serializer **MUST** satify the interface defined by
    ``EnvelopeItemSerializer``.
    """

    def envelope_for(self, item):
        """Return an envelope containing caching headers and other properties for the
        ``item`` being serialized, as well as the serialized representation of the
        ``item``.
        """
        return {
            "href": self.child.absolute_url_for(item),
            "etag": self.child.etag_for(item),
            "last_modified": self.child.last_modified_for(item),
            "schema": self.child.schema_url(),
            "ld_context": self.child.ld_context_url(),
            "content": self.child.to_representation(item),
        }

    def to_representation(self, data):
        """Return the serialized representation of the list with every item in the list
        wrapped in an envelope containing the caching headers and other properties
        associated with each item in the list.
        """
        iterable = data.all() if isinstance(data, (Manager, QuerySet)) else data
        ret = [self.envelope_for(item) for item in iterable]
        return ret
