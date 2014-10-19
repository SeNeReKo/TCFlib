#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Frederik Elwert <frederik.elwert@web.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This module provides an API for common linguistic tagsets as used in TCF.

"""
from lxml import etree

NS_DCIF = 'http://www.isocat.org/ns/dcif'
P_DCIF = '{' + NS_DCIF + '}'
NS = {'dcif': NS_DCIF}
tagsets = {}


class TagBase(object):
    """
    Base class for Tags.

    """

    def __str__(self):
        return '<Tag "{}">'.format(self.name)

    def is_a(self, tag):
        """
        Tests if the tag is the same or a child of the given tag.

        :param tag: The tag to compare to.

        """
        raise NotImplementedError


class TagSetBase(object):
    """
    Base class for TagSets.

    """

    def __str__(self):
        return '<TagSet "{}">'.format(self.name)

    def __getitem__(self, token):
        tag = self.find_tag(name=token)
        if tag is None:
            tag = self.find_tag(pid=token)
        if tag is None:
            raise KeyError('no tag "{}" in tagset.'.format(token))
        else:
            return tag

    def find_tag(self, name=None, pid=None):
        """Finds a tag by name or PID.

        Either pass `name` or `pid`, but not both.

        """
        raise NotImplementedError

    def find_all_tags(self):
        """Returns all tags in the tagset."""
        raise NotImplementedError


class ISOcatTag(TagBase, etree.ElementBase):
    """
    Base class for ISOcat Tags.

    """

    _name_xpath = etree.XPath('string(dcif:administrationInformationSection/'
        'dcif:administrationRecord/'
        'dcif:identifier[1])',
        namespaces=NS)

    def __hash__(self):
        return hash(self.pid)

    def __eq__(self, other):
        return self.pid == other.pid

    def __str__(self):
        return '<Tag "{}" {{{}}}>'.format(self.name, self.pid)

    @property
    def pid(self):
        return self.get('pid')

    @property
    def name(self):
        return self._name_xpath(self)

    def is_a(self, tag):
        return tag == self or tag in self.find_all_super()

    def find_super(self):
        """Returns the parent tag (or None)."""
        isa = self.find(P_DCIF + 'isA')
        if isa is not None:
            return ISOcatTagSet._by_pid_xpath(self, pid=isa.get('pid'))[0]

    def find_all_super(self):
        """Returns a list of all ancestor tags."""
        supers = []
        super_tag = self.find_super()
        while super_tag is not None:
            supers.append(super_tag)
            super_tag = super_tag.find_super()
        return supers

    def find_top(self):
        """Returns the top-most ancestor tag (or self)."""
        supers = self.find_all_super()
        if supers:
            return supers[-1]
        else:
            return self


class ISOcatTagSet(TagSetBase):
    """
    Base class for ISOcat TagSets.

    """

    __file__ = ''
    name = ''
    pid = ''
    tag_class = ISOcatTag

    _by_pid_xpath = etree.XPath('//dcif:dataCategory['
        '@pid = $pid][1]',
        namespaces=NS)
    _by_name_xpath = etree.XPath('//dcif:dataCategory['
        'dcif:administrationInformationSection/'
        'dcif:administrationRecord/'
        'dcif:identifier = $name][1]',
        namespaces=NS)
    _all_from_domain = etree.XPath('/dcif:dataCategorySelection/'
        'dcif:dataCategory[@pid='
            '/dcif:dataCategorySelection/dcif:dataCategory[@pid=$pid]/'
            'dcif:conceptualDomain[dcif:profile=$profile]/dcif:value/@pid]',
        namespaces=NS)

    def __init__(self):
        lookup = etree.ElementNamespaceClassLookup()
        parser = etree.XMLParser(remove_blank_text=True)
        parser.set_element_class_lookup(lookup)

        namespace = lookup.get_namespace(NS_DCIF)
        namespace['dataCategory'] = self.tag_class
        self._tree = etree.parse(self.__file__, parser=parser)

    def __str__(self):
        return '<TagSet "{}" {{{}}}>'.format(self.name, self.pid)

    def find_tag(self, name=None, pid=None):
        if name and pid:
            raise TypeError('method "find_tag" of class "{}" expects "name" '
                            'or "pid", got both.'.format(type(self)))
        if not name and not pid:
            raise TypeError('method "find_tag" of class "{}" expects "name" '
                            'or "pid".'.format(type(self)))
        if name:
            result = self._by_name_xpath(self._tree, name=name)
        elif pid:
            result = self._by_pid_xpath(self._tree, pid=pid)
        if result:
            return result[0]
        else:
            return None

    def find_all_tags(self, profile):
        return self._all_from_domain(self._tree, pid=self.pid, profile=profile)


class MappingTag(ISOcatTag):
    """
    A Tag that maps names to ISOcat pids.

    See the `MappingTagSet` for description.

    """
    name2pid = {}
    pid2name = {}

    @property
    def name(self):
        try:
            return self.pid2name[self.pid]
        except KeyError:
            # There is no explicit mapping for the PID, return the ISOcat name.
            return super().name


class MappingTagSet(ISOcatTagSet):
    """
    A TagSet that maps names to ISOcat pids.

    This base class can be used to create TagSets with name aliases for
    ISOcat TagSets. This way, arbitrary TagSets can be modeled onto ISOcat,
    getting e.g. hierarchy information from ISOcat while using established
    names.

    """
    tag_class = MappingTag

    def find_tag(self, name=None, pid=None):
        if name and pid:
            raise TypeError('method "find_tag" of class "{}" expects "name" '
                            'or "pid", got both.'.format(type(self)))
        if not name and not pid:
            raise TypeError('method "find_tag" of class "{}" expects "name" '
                            'or "pid".'.format(type(self)))
        if name:
            pid = self.tag_class.name2pid[name]
        return super().find_tag(pid=pid)


class POSTagBase(ISOcatTag):
    """
    Base class for ISOcat Part-of-Speech-Tags.

    """

    @property
    def is_closed(self):
        """If the tag is defined as a closed word class."""
        if self.pid in self.CLOSED:
            return True
        for super_tag in self.find_all_super():
            if super_tag.pid in self.CLOSED:
                return True
        return False


class POSTagSetBase(ISOcatTagSet):
    """
    Base class for ISOcat Part-of-Speech-TagSets.

    """
    pass


def register_tagset(tagset_class):
    """
    Register a TagSet class.

    Registered TagSets can be looked up by their name.

    """
    tagsets[tagset_class.name.lower()] = {'class': tagset_class}


def TagSet(name):
    """
    Return a TagSet instance for a given name.

    """
    # To save initialization (which might involve I/O and XML parsing), this
    # function returns always the same instance.
    key = name.lower()
    if 'instance' not in tagsets[key]:
        tagsets[key]['instance'] = tagsets[key]['class']()
    return tagsets[key]['instance']
