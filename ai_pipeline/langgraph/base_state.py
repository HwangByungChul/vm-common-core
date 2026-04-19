from typing import TypedDict, List, Optional, Annotated, Any
import operator

def merge_list(left: list, right: list) -> list:
    """리스트를 병합하는 리듀서 함수"""
    return left + right

class BaseAgentState(TypedDict):
    """
    LangGraph 에이전트의 기본 상태 구조.
    각 프로젝트에서 이를 상속받아 필요한 필드를 추가합니다.
    """
    messages: Annotated[List[Any], operator.add]
    context: str
    error: Optional[str]
    metadata: dict
    next_node: Optional[str]
