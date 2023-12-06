from typing import Optional, List, Tuple
from pydantic import BaseModel
from langchain.schema.messages import HumanMessage, AIMessage
from langchain.chains import LLMChain
from langchain.chat_models.base import BaseChatModel
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

from common.callbacks.stream_handler import StreamingCallbackHandler


class ChatOutput(BaseModel):
    answer: str
    sql_query: Optional[str] = None


class Chatter:
    # searcher: VectorStore
    chat_llm: BaseChatModel
    # condense_llm: BaseLanguageModel
    # max_token_limit: Optional[int]

    # _schemas_var_name: str = "schemas"
    # TODO: add schema format into the template
    _chat_system_template: str = """You are an assistant of Gonswap, a decentralized exchange on the X1 network. You \
main job is to answer the user's question."""
    _chat_human_template: str = "{question}"
    # _no_docs_found_response: str = "Sorry I can not respond to your question."
    # _condense_template: str = """Given the following conversation, rephrase the follow up question to be a \
# standalone \
# question. The standalone question must be in English.
# ---
# Conversation:
# {chat_history}
#
# Follow up question: {question}
#
# Standalone question:"""

    # _question_pattern: Pattern = compile(r"#### ([^\n]+)$")

    def __init__(
        self,
        *,
        # searcher: VectorStore,
        chat_llm: BaseChatModel,
        # condense_llm: Optional[BaseLanguageModel] = None,
        # max_token_limit: Optional[int] = None,
    ):
        # self.searcher = searcher
        self.chat_llm = chat_llm
        # self.condense_llm = condense_llm or chat_llm
        # self.max_token_limit = max_token_limit

    def _build_chat_prompt(self, chat_history: List[Tuple[str, str]]) -> ChatPromptTemplate:
        messages = [SystemMessagePromptTemplate.from_template(self._chat_system_template)]
        for q, a in chat_history:
            messages.append(HumanMessage(content=q))
            messages.append(AIMessage(content=a))
        messages.append(HumanMessagePromptTemplate.from_template(self._chat_human_template))
        return ChatPromptTemplate.from_messages(messages)

    # def _build_chat_chain(
    #     self,
    #     chat_prompt: ChatPromptTemplate,
    #     return_docs: bool,
    #     return_gen_question: bool,
    #     stream: bool,
    #     **search_args,
    # ) -> QARetrievalChain:
    #     llm_chain = LLMChain(
    #         prompt=chat_prompt,
    #         llm=self.chat_llm,
    #         llm_kwargs=dict(stream=stream),
    #     )
    #     schemas_chain = CombineSchemasChain(
    #         llm_chain=llm_chain,
    #         schemas_var_name=self._schemas_var_name,
    #     )
    #     condense_chain = LLMChain(
    #         llm=self.condense_llm,
    #         prompt=PromptTemplate.from_template(self._condense_template),
    #     )
    #     return QARetrievalChain(
    #         retriever=self.searcher.as_retriever(**search_args),
    #         max_tokens_limit=self.max_token_limit,
    #         combine_docs_chain=schemas_chain,
    #         question_generator=condense_chain,
    #         rephrase_question=False,
    #         return_source_documents=return_docs,
    #         return_generated_question=return_gen_question,
    #         # response_if_no_docs_found=self._no_docs_found_response,
    #     )

    async def chat(
        self,
        question: str,
        chat_history: List[Tuple[str, str]],
        *,
        stream_handler: Optional[StreamingCallbackHandler] = None,
    ) -> ChatOutput:
        chat_prompt = self._build_chat_prompt(chat_history)
        chat_chain = LLMChain(
            prompt=chat_prompt,
            llm=self.chat_llm,
            llm_kwargs=dict(stream=stream_handler is not None),
        )
        output = await chat_chain.acall(
            inputs=dict(
                question=question,
                chat_history=chat_history,
            ),
            return_only_outputs=True,
            callbacks=[stream_handler] if stream_handler else None,
        )

        answer = output[chat_chain.output_key]
        return ChatOutput(answer=answer)
