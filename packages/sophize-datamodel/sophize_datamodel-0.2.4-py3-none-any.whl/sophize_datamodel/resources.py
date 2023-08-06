
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from enum import Enum


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


class Citation:
    text_citation: Optional[str]

    def __init__(self, text_citation: Optional[str]) -> None:
        self.text_citation = text_citation

    @staticmethod
    def from_dict(obj: Any) -> 'Citation':
        assert isinstance(obj, dict)
        text_citation = from_union([from_str, from_none], obj.get("textCitation"))
        return Citation(text_citation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["textCitation"] = from_union([from_str, from_none], self.text_citation)
        return result


class User:
    handle: Optional[str]
    user_email: Optional[str]
    user_link: Optional[str]
    user_name: Optional[str]
    user_pic: Optional[str]

    def __init__(self, handle: Optional[str], user_email: Optional[str], user_link: Optional[str], user_name: Optional[str], user_pic: Optional[str]) -> None:
        self.handle = handle
        self.user_email = user_email
        self.user_link = user_link
        self.user_name = user_name
        self.user_pic = user_pic

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        handle = from_union([from_str, from_none], obj.get("handle"))
        user_email = from_union([from_str, from_none], obj.get("userEmail"))
        user_link = from_union([from_str, from_none], obj.get("userLink"))
        user_name = from_union([from_str, from_none], obj.get("userName"))
        user_pic = from_union([from_str, from_none], obj.get("userPic"))
        return User(handle, user_email, user_link, user_name, user_pic)

    def to_dict(self) -> dict:
        result: dict = {}
        result["handle"] = from_union([from_str, from_none], self.handle)
        result["userEmail"] = from_union([from_str, from_none], self.user_email)
        result["userLink"] = from_union([from_str, from_none], self.user_link)
        result["userName"] = from_union([from_str, from_none], self.user_name)
        result["userPic"] = from_union([from_str, from_none], self.user_pic)
        return result


class Language(Enum):
    INFORMAL = "INFORMAL"
    METAMATH_SET_MM = "METAMATH_SET_MM"


class MetaLanguage(Enum):
    INFORMAL = "INFORMAL"
    METAMATH = "METAMATH"


class Argument:
    argument_text: Optional[str]
    conclusion: Optional[str]
    language: Optional[Language]
    lookup_terms: Optional[List[str]]
    meta_language: Optional[MetaLanguage]
    premise_machine: Optional[str]
    premises: Optional[List[str]]
    assignable_ptr: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    ephemeral_ptr: Optional[str]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, argument_text: Optional[str], conclusion: Optional[str], language: Optional[Language], lookup_terms: Optional[List[str]], meta_language: Optional[MetaLanguage], premise_machine: Optional[str], premises: Optional[List[str]], assignable_ptr: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], ephemeral_ptr: Optional[str], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.argument_text = argument_text
        self.conclusion = conclusion
        self.language = language
        self.lookup_terms = lookup_terms
        self.meta_language = meta_language
        self.premise_machine = premise_machine
        self.premises = premises
        self.assignable_ptr = assignable_ptr
        self.citations = citations
        self.contributor = contributor
        self.ephemeral_ptr = ephemeral_ptr
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Argument':
        assert isinstance(obj, dict)
        argument_text = from_union([from_str, from_none], obj.get("argumentText"))
        conclusion = from_union([from_str, from_none], obj.get("conclusion"))
        language = from_union([Language, from_none], obj.get("language"))
        lookup_terms = from_union([lambda x: from_list(from_str, x), from_none], obj.get("lookupTerms"))
        meta_language = from_union([MetaLanguage, from_none], obj.get("metaLanguage"))
        premise_machine = from_union([from_str, from_none], obj.get("premiseMachine"))
        premises = from_union([lambda x: from_list(from_str, x), from_none], obj.get("premises"))
        assignable_ptr = from_union([from_str, from_none], obj.get("assignablePtr"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        ephemeral_ptr = from_union([from_str, from_none], obj.get("ephemeralPtr"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Argument(argument_text, conclusion, language, lookup_terms, meta_language, premise_machine, premises, assignable_ptr, citations, contributor, ephemeral_ptr, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["argumentText"] = from_union([from_str, from_none], self.argument_text)
        result["conclusion"] = from_union([from_str, from_none], self.conclusion)
        result["language"] = from_union([lambda x: to_enum(Language, x), from_none], self.language)
        result["lookupTerms"] = from_union([lambda x: from_list(from_str, x), from_none], self.lookup_terms)
        result["metaLanguage"] = from_union([lambda x: to_enum(MetaLanguage, x), from_none], self.meta_language)
        result["premiseMachine"] = from_union([from_str, from_none], self.premise_machine)
        result["premises"] = from_union([lambda x: from_list(from_str, x), from_none], self.premises)
        result["assignablePtr"] = from_union([from_str, from_none], self.assignable_ptr)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["ephemeralPtr"] = from_union([from_str, from_none], self.ephemeral_ptr)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Author:
    user: Optional[User]

    def __init__(self, user: Optional[User]) -> None:
        self.user = user

    @staticmethod
    def from_dict(obj: Any) -> 'Author':
        assert isinstance(obj, dict)
        user = from_union([User.from_dict, from_none], obj.get("user"))
        return Author(user)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user"] = from_union([lambda x: to_class(User, x), from_none], self.user)
        return result


class Article:
    abstract_text: Optional[str]
    authors: Optional[List[Author]]
    beliefset: Optional[str]
    content: Optional[str]
    title: Optional[str]
    assignable_ptr: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    ephemeral_ptr: Optional[str]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, abstract_text: Optional[str], authors: Optional[List[Author]], beliefset: Optional[str], content: Optional[str], title: Optional[str], assignable_ptr: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], ephemeral_ptr: Optional[str], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.abstract_text = abstract_text
        self.authors = authors
        self.beliefset = beliefset
        self.content = content
        self.title = title
        self.assignable_ptr = assignable_ptr
        self.citations = citations
        self.contributor = contributor
        self.ephemeral_ptr = ephemeral_ptr
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Article':
        assert isinstance(obj, dict)
        abstract_text = from_union([from_str, from_none], obj.get("abstractText"))
        authors = from_union([lambda x: from_list(Author.from_dict, x), from_none], obj.get("authors"))
        beliefset = from_union([from_str, from_none], obj.get("beliefset"))
        content = from_union([from_str, from_none], obj.get("content"))
        title = from_union([from_str, from_none], obj.get("title"))
        assignable_ptr = from_union([from_str, from_none], obj.get("assignablePtr"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        ephemeral_ptr = from_union([from_str, from_none], obj.get("ephemeralPtr"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Article(abstract_text, authors, beliefset, content, title, assignable_ptr, citations, contributor, ephemeral_ptr, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["abstractText"] = from_union([from_str, from_none], self.abstract_text)
        result["authors"] = from_union([lambda x: from_list(lambda x: to_class(Author, x), x), from_none], self.authors)
        result["beliefset"] = from_union([from_str, from_none], self.beliefset)
        result["content"] = from_union([from_str, from_none], self.content)
        result["title"] = from_union([from_str, from_none], self.title)
        result["assignablePtr"] = from_union([from_str, from_none], self.assignable_ptr)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["ephemeralPtr"] = from_union([from_str, from_none], self.ephemeral_ptr)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Beliefset:
    sub_beliefset_ptrs: Optional[List[str]]
    unsupported_machine_ptrs: Optional[List[str]]
    unsupported_proposition_ptrs: Optional[List[str]]
    assignable_ptr: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    ephemeral_ptr: Optional[str]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, sub_beliefset_ptrs: Optional[List[str]], unsupported_machine_ptrs: Optional[List[str]], unsupported_proposition_ptrs: Optional[List[str]], assignable_ptr: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], ephemeral_ptr: Optional[str], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.sub_beliefset_ptrs = sub_beliefset_ptrs
        self.unsupported_machine_ptrs = unsupported_machine_ptrs
        self.unsupported_proposition_ptrs = unsupported_proposition_ptrs
        self.assignable_ptr = assignable_ptr
        self.citations = citations
        self.contributor = contributor
        self.ephemeral_ptr = ephemeral_ptr
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Beliefset':
        assert isinstance(obj, dict)
        sub_beliefset_ptrs = from_union([lambda x: from_list(from_str, x), from_none], obj.get("subBeliefsetPtrs"))
        unsupported_machine_ptrs = from_union([lambda x: from_list(from_str, x), from_none], obj.get("unsupportedMachinePtrs"))
        unsupported_proposition_ptrs = from_union([lambda x: from_list(from_str, x), from_none], obj.get("unsupportedPropositionPtrs"))
        assignable_ptr = from_union([from_str, from_none], obj.get("assignablePtr"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        ephemeral_ptr = from_union([from_str, from_none], obj.get("ephemeralPtr"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Beliefset(sub_beliefset_ptrs, unsupported_machine_ptrs, unsupported_proposition_ptrs, assignable_ptr, citations, contributor, ephemeral_ptr, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["subBeliefsetPtrs"] = from_union([lambda x: from_list(from_str, x), from_none], self.sub_beliefset_ptrs)
        result["unsupportedMachinePtrs"] = from_union([lambda x: from_list(from_str, x), from_none], self.unsupported_machine_ptrs)
        result["unsupportedPropositionPtrs"] = from_union([lambda x: from_list(from_str, x), from_none], self.unsupported_proposition_ptrs)
        result["assignablePtr"] = from_union([from_str, from_none], self.assignable_ptr)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["ephemeralPtr"] = from_union([from_str, from_none], self.ephemeral_ptr)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Machine:
    default_language: Optional[Language]
    default_lenient_statement: Optional[str]
    default_materialize_dataset: Optional[str]
    default_strict_statement: Optional[str]
    description: Optional[str]
    premise_machines: Optional[List[str]]
    premise_propositions: Optional[List[str]]
    server_name: Optional[str]
    assignable_ptr: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    ephemeral_ptr: Optional[str]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, default_language: Optional[Language], default_lenient_statement: Optional[str], default_materialize_dataset: Optional[str], default_strict_statement: Optional[str], description: Optional[str], premise_machines: Optional[List[str]], premise_propositions: Optional[List[str]], server_name: Optional[str], assignable_ptr: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], ephemeral_ptr: Optional[str], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.default_language = default_language
        self.default_lenient_statement = default_lenient_statement
        self.default_materialize_dataset = default_materialize_dataset
        self.default_strict_statement = default_strict_statement
        self.description = description
        self.premise_machines = premise_machines
        self.premise_propositions = premise_propositions
        self.server_name = server_name
        self.assignable_ptr = assignable_ptr
        self.citations = citations
        self.contributor = contributor
        self.ephemeral_ptr = ephemeral_ptr
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Machine':
        assert isinstance(obj, dict)
        default_language = from_union([Language, from_none], obj.get("defaultLanguage"))
        default_lenient_statement = from_union([from_str, from_none], obj.get("defaultLenientStatement"))
        default_materialize_dataset = from_union([from_str, from_none], obj.get("defaultMaterializeDataset"))
        default_strict_statement = from_union([from_str, from_none], obj.get("defaultStrictStatement"))
        description = from_union([from_str, from_none], obj.get("description"))
        premise_machines = from_union([lambda x: from_list(from_str, x), from_none], obj.get("premiseMachines"))
        premise_propositions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("premisePropositions"))
        server_name = from_union([from_str, from_none], obj.get("serverName"))
        assignable_ptr = from_union([from_str, from_none], obj.get("assignablePtr"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        ephemeral_ptr = from_union([from_str, from_none], obj.get("ephemeralPtr"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Machine(default_language, default_lenient_statement, default_materialize_dataset, default_strict_statement, description, premise_machines, premise_propositions, server_name, assignable_ptr, citations, contributor, ephemeral_ptr, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["defaultLanguage"] = from_union([lambda x: to_enum(Language, x), from_none], self.default_language)
        result["defaultLenientStatement"] = from_union([from_str, from_none], self.default_lenient_statement)
        result["defaultMaterializeDataset"] = from_union([from_str, from_none], self.default_materialize_dataset)
        result["defaultStrictStatement"] = from_union([from_str, from_none], self.default_strict_statement)
        result["description"] = from_union([from_str, from_none], self.description)
        result["premiseMachines"] = from_union([lambda x: from_list(from_str, x), from_none], self.premise_machines)
        result["premisePropositions"] = from_union([lambda x: from_list(from_str, x), from_none], self.premise_propositions)
        result["serverName"] = from_union([from_str, from_none], self.server_name)
        result["assignablePtr"] = from_union([from_str, from_none], self.assignable_ptr)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["ephemeralPtr"] = from_union([from_str, from_none], self.ephemeral_ptr)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Page:
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    description: Optional[str]
    page_id: Optional[str]
    parent_page_id: Optional[str]
    sort_hint: Optional[float]
    title: Optional[str]

    def __init__(self, citations: Optional[List[Citation]], contributor: Optional[User], description: Optional[str], page_id: Optional[str], parent_page_id: Optional[str], sort_hint: Optional[float], title: Optional[str]) -> None:
        self.citations = citations
        self.contributor = contributor
        self.description = description
        self.page_id = page_id
        self.parent_page_id = parent_page_id
        self.sort_hint = sort_hint
        self.title = title

    @staticmethod
    def from_dict(obj: Any) -> 'Page':
        assert isinstance(obj, dict)
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        description = from_union([from_str, from_none], obj.get("description"))
        page_id = from_union([from_str, from_none], obj.get("pageId"))
        parent_page_id = from_union([from_str, from_none], obj.get("parentPageId"))
        sort_hint = from_union([from_float, from_none], obj.get("sortHint"))
        title = from_union([from_str, from_none], obj.get("title"))
        return Page(citations, contributor, description, page_id, parent_page_id, sort_hint, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["description"] = from_union([from_str, from_none], self.description)
        result["pageId"] = from_union([from_str, from_none], self.page_id)
        result["parentPageId"] = from_union([from_str, from_none], self.parent_page_id)
        result["sortHint"] = from_union([to_float, from_none], self.sort_hint)
        result["title"] = from_union([from_str, from_none], self.title)
        return result


class Project:
    abstract_text: Optional[str]
    description: Optional[str]
    assignable_ptr: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    ephemeral_ptr: Optional[str]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, abstract_text: Optional[str], description: Optional[str], assignable_ptr: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], ephemeral_ptr: Optional[str], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.abstract_text = abstract_text
        self.description = description
        self.assignable_ptr = assignable_ptr
        self.citations = citations
        self.contributor = contributor
        self.ephemeral_ptr = ephemeral_ptr
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Project':
        assert isinstance(obj, dict)
        abstract_text = from_union([from_str, from_none], obj.get("abstractText"))
        description = from_union([from_str, from_none], obj.get("description"))
        assignable_ptr = from_union([from_str, from_none], obj.get("assignablePtr"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        ephemeral_ptr = from_union([from_str, from_none], obj.get("ephemeralPtr"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Project(abstract_text, description, assignable_ptr, citations, contributor, ephemeral_ptr, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["abstractText"] = from_union([from_str, from_none], self.abstract_text)
        result["description"] = from_union([from_str, from_none], self.description)
        result["assignablePtr"] = from_union([from_str, from_none], self.assignable_ptr)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["ephemeralPtr"] = from_union([from_str, from_none], self.ephemeral_ptr)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class Proposition:
    language: Optional[Language]
    lookup_terms: Optional[List[str]]
    meta_language: Optional[MetaLanguage]
    negative_statement: Optional[str]
    remarks: Optional[str]
    statement: Optional[str]
    assignable_ptr: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    ephemeral_ptr: Optional[str]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, language: Optional[Language], lookup_terms: Optional[List[str]], meta_language: Optional[MetaLanguage], negative_statement: Optional[str], remarks: Optional[str], statement: Optional[str], assignable_ptr: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], ephemeral_ptr: Optional[str], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.language = language
        self.lookup_terms = lookup_terms
        self.meta_language = meta_language
        self.negative_statement = negative_statement
        self.remarks = remarks
        self.statement = statement
        self.assignable_ptr = assignable_ptr
        self.citations = citations
        self.contributor = contributor
        self.ephemeral_ptr = ephemeral_ptr
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Proposition':
        assert isinstance(obj, dict)
        language = from_union([Language, from_none], obj.get("language"))
        lookup_terms = from_union([lambda x: from_list(from_str, x), from_none], obj.get("lookupTerms"))
        meta_language = from_union([MetaLanguage, from_none], obj.get("metaLanguage"))
        negative_statement = from_union([from_str, from_none], obj.get("negativeStatement"))
        remarks = from_union([from_str, from_none], obj.get("remarks"))
        statement = from_union([from_str, from_none], obj.get("statement"))
        assignable_ptr = from_union([from_str, from_none], obj.get("assignablePtr"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        ephemeral_ptr = from_union([from_str, from_none], obj.get("ephemeralPtr"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Proposition(language, lookup_terms, meta_language, negative_statement, remarks, statement, assignable_ptr, citations, contributor, ephemeral_ptr, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["language"] = from_union([lambda x: to_enum(Language, x), from_none], self.language)
        result["lookupTerms"] = from_union([lambda x: from_list(from_str, x), from_none], self.lookup_terms)
        result["metaLanguage"] = from_union([lambda x: to_enum(MetaLanguage, x), from_none], self.meta_language)
        result["negativeStatement"] = from_union([from_str, from_none], self.negative_statement)
        result["remarks"] = from_union([from_str, from_none], self.remarks)
        result["statement"] = from_union([from_str, from_none], self.statement)
        result["assignablePtr"] = from_union([from_str, from_none], self.assignable_ptr)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["ephemeralPtr"] = from_union([from_str, from_none], self.ephemeral_ptr)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


class ProofRequest:
    fetch_proof: Optional[bool]
    fetch_updated_proposition: Optional[bool]
    machine_ptr: Optional[str]
    parse_lenient: Optional[bool]
    proposition: Optional[Proposition]

    def __init__(self, fetch_proof: Optional[bool], fetch_updated_proposition: Optional[bool], machine_ptr: Optional[str], parse_lenient: Optional[bool], proposition: Optional[Proposition]) -> None:
        self.fetch_proof = fetch_proof
        self.fetch_updated_proposition = fetch_updated_proposition
        self.machine_ptr = machine_ptr
        self.parse_lenient = parse_lenient
        self.proposition = proposition

    @staticmethod
    def from_dict(obj: Any) -> 'ProofRequest':
        assert isinstance(obj, dict)
        fetch_proof = from_union([from_bool, from_none], obj.get("fetchProof"))
        fetch_updated_proposition = from_union([from_bool, from_none], obj.get("fetchUpdatedProposition"))
        machine_ptr = from_union([from_str, from_none], obj.get("machinePtr"))
        parse_lenient = from_union([from_bool, from_none], obj.get("parseLenient"))
        proposition = from_union([Proposition.from_dict, from_none], obj.get("proposition"))
        return ProofRequest(fetch_proof, fetch_updated_proposition, machine_ptr, parse_lenient, proposition)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fetchProof"] = from_union([from_bool, from_none], self.fetch_proof)
        result["fetchUpdatedProposition"] = from_union([from_bool, from_none], self.fetch_updated_proposition)
        result["machinePtr"] = from_union([from_str, from_none], self.machine_ptr)
        result["parseLenient"] = from_union([from_bool, from_none], self.parse_lenient)
        result["proposition"] = from_union([lambda x: to_class(Proposition, x), from_none], self.proposition)
        return result


class TruthValue(Enum):
    CONTRADICTION = "CONTRADICTION"
    FALSE = "FALSE"
    TRUE = "TRUE"
    UNKNOWN = "UNKNOWN"


class ProofResponse:
    existing_proposition_ptr: Optional[str]
    message: Optional[str]
    proof_arguments: Optional[List[Argument]]
    proof_propositions: Optional[List[Proposition]]
    resolved_proposition: Optional[Proposition]
    truth_value: Optional[TruthValue]

    def __init__(self, existing_proposition_ptr: Optional[str], message: Optional[str], proof_arguments: Optional[List[Argument]], proof_propositions: Optional[List[Proposition]], resolved_proposition: Optional[Proposition], truth_value: Optional[TruthValue]) -> None:
        self.existing_proposition_ptr = existing_proposition_ptr
        self.message = message
        self.proof_arguments = proof_arguments
        self.proof_propositions = proof_propositions
        self.resolved_proposition = resolved_proposition
        self.truth_value = truth_value

    @staticmethod
    def from_dict(obj: Any) -> 'ProofResponse':
        assert isinstance(obj, dict)
        existing_proposition_ptr = from_union([from_str, from_none], obj.get("existingPropositionPtr"))
        message = from_union([from_str, from_none], obj.get("message"))
        proof_arguments = from_union([lambda x: from_list(Argument.from_dict, x), from_none], obj.get("proofArguments"))
        proof_propositions = from_union([lambda x: from_list(Proposition.from_dict, x), from_none], obj.get("proofPropositions"))
        resolved_proposition = from_union([Proposition.from_dict, from_none], obj.get("resolvedProposition"))
        truth_value = from_union([TruthValue, from_none], obj.get("truthValue"))
        return ProofResponse(existing_proposition_ptr, message, proof_arguments, proof_propositions, resolved_proposition, truth_value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["existingPropositionPtr"] = from_union([from_str, from_none], self.existing_proposition_ptr)
        result["message"] = from_union([from_str, from_none], self.message)
        result["proofArguments"] = from_union([lambda x: from_list(lambda x: to_class(Argument, x), x), from_none], self.proof_arguments)
        result["proofPropositions"] = from_union([lambda x: from_list(lambda x: to_class(Proposition, x), x), from_none], self.proof_propositions)
        result["resolvedProposition"] = from_union([lambda x: to_class(Proposition, x), from_none], self.resolved_proposition)
        result["truthValue"] = from_union([lambda x: to_enum(TruthValue, x), from_none], self.truth_value)
        return result


class Term:
    alternate_phrases: Optional[List[str]]
    definition: Optional[str]
    language: Optional[Language]
    lookup_terms: Optional[List[str]]
    meta_language: Optional[MetaLanguage]
    phrase: Optional[str]
    primitive: Optional[bool]
    remarks: Optional[str]
    assignable_ptr: Optional[str]
    citations: Optional[List[Citation]]
    contributor: Optional[User]
    ephemeral_ptr: Optional[str]
    indexable: Optional[bool]
    names: Optional[List[str]]
    not_permanent_ptr: Optional[str]
    permanent_ptr: Optional[str]
    tags: Optional[List[str]]

    def __init__(self, alternate_phrases: Optional[List[str]], definition: Optional[str], language: Optional[Language], lookup_terms: Optional[List[str]], meta_language: Optional[MetaLanguage], phrase: Optional[str], primitive: Optional[bool], remarks: Optional[str], assignable_ptr: Optional[str], citations: Optional[List[Citation]], contributor: Optional[User], ephemeral_ptr: Optional[str], indexable: Optional[bool], names: Optional[List[str]], not_permanent_ptr: Optional[str], permanent_ptr: Optional[str], tags: Optional[List[str]]) -> None:
        self.alternate_phrases = alternate_phrases
        self.definition = definition
        self.language = language
        self.lookup_terms = lookup_terms
        self.meta_language = meta_language
        self.phrase = phrase
        self.primitive = primitive
        self.remarks = remarks
        self.assignable_ptr = assignable_ptr
        self.citations = citations
        self.contributor = contributor
        self.ephemeral_ptr = ephemeral_ptr
        self.indexable = indexable
        self.names = names
        self.not_permanent_ptr = not_permanent_ptr
        self.permanent_ptr = permanent_ptr
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> 'Term':
        assert isinstance(obj, dict)
        alternate_phrases = from_union([lambda x: from_list(from_str, x), from_none], obj.get("alternatePhrases"))
        definition = from_union([from_str, from_none], obj.get("definition"))
        language = from_union([Language, from_none], obj.get("language"))
        lookup_terms = from_union([lambda x: from_list(from_str, x), from_none], obj.get("lookupTerms"))
        meta_language = from_union([MetaLanguage, from_none], obj.get("metaLanguage"))
        phrase = from_union([from_str, from_none], obj.get("phrase"))
        primitive = from_union([from_bool, from_none], obj.get("primitive"))
        remarks = from_union([from_str, from_none], obj.get("remarks"))
        assignable_ptr = from_union([from_str, from_none], obj.get("assignablePtr"))
        citations = from_union([lambda x: from_list(Citation.from_dict, x), from_none], obj.get("citations"))
        contributor = from_union([User.from_dict, from_none], obj.get("contributor"))
        ephemeral_ptr = from_union([from_str, from_none], obj.get("ephemeralPtr"))
        indexable = from_union([from_bool, from_none], obj.get("indexable"))
        names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("names"))
        not_permanent_ptr = from_union([from_str, from_none], obj.get("notPermanentPtr"))
        permanent_ptr = from_union([from_str, from_none], obj.get("permanentPtr"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Term(alternate_phrases, definition, language, lookup_terms, meta_language, phrase, primitive, remarks, assignable_ptr, citations, contributor, ephemeral_ptr, indexable, names, not_permanent_ptr, permanent_ptr, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["alternatePhrases"] = from_union([lambda x: from_list(from_str, x), from_none], self.alternate_phrases)
        result["definition"] = from_union([from_str, from_none], self.definition)
        result["language"] = from_union([lambda x: to_enum(Language, x), from_none], self.language)
        result["lookupTerms"] = from_union([lambda x: from_list(from_str, x), from_none], self.lookup_terms)
        result["metaLanguage"] = from_union([lambda x: to_enum(MetaLanguage, x), from_none], self.meta_language)
        result["phrase"] = from_union([from_str, from_none], self.phrase)
        result["primitive"] = from_union([from_bool, from_none], self.primitive)
        result["remarks"] = from_union([from_str, from_none], self.remarks)
        result["assignablePtr"] = from_union([from_str, from_none], self.assignable_ptr)
        result["citations"] = from_union([lambda x: from_list(lambda x: to_class(Citation, x), x), from_none], self.citations)
        result["contributor"] = from_union([lambda x: to_class(User, x), from_none], self.contributor)
        result["ephemeralPtr"] = from_union([from_str, from_none], self.ephemeral_ptr)
        result["indexable"] = from_union([from_bool, from_none], self.indexable)
        result["names"] = from_union([lambda x: from_list(from_str, x), from_none], self.names)
        result["notPermanentPtr"] = from_union([from_str, from_none], self.not_permanent_ptr)
        result["permanentPtr"] = from_union([from_str, from_none], self.permanent_ptr)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


