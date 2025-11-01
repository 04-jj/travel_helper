import dotenv
import yaml
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from clothes_recommender import clothes_recommender
from route_agent import route_planning
from visit_agent import visit_recommender
from weather_agent import get_weather

dotenv.load_dotenv()


def get_clothes_recommendation(city):
    weather = get_weather(city)
    if "失败" in weather:
        return f"无法获取天气信息，请检查城市名是否正确"

    clothes_advice = clothes_recommender(weather)
    return f"\n\n{clothes_advice}\n\n"


class TravelHelper:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
        )

        self.tools = [
            Tool(
                func=get_weather,
                name="weather_query",
                description="查询天气信息"
            ),

            Tool(
                func=route_planning,
                name="route_planning",
                description="进行驾车路径规划"
            ),

            Tool(
                func=visit_recommender,
                name="visit_recommendation",
                description="推荐城市景点",
            ),

            Tool(
                func=clothes_recommender,
                name="clothes_recommendation",
                description="基于天气进行穿搭建议"
            ),
        ]

        with open('prompt.yaml', 'r', encoding='utf-8') as f:
            prompt = yaml.safe_load(f)

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system",prompt['system_prompt']),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        self.agent = create_tool_calling_agent(
            llm=self.llm,
            prompt=self.prompt_template,
            tools=self.tools,
        )

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            memory=self.memory,
            tools=self.tools,
            verbose=True,
        )

    def chat(self, inputs):
        res = self.agent_executor.invoke({
            "input": inputs,
        })

        return res['output']


if __name__ == '__main__':
    travelHelper = TravelHelper()

    print("您好，我是旅游服务智能助手，请问有什么可以帮助您？")
    while True:
        user_input = input("用户提问：").strip()

        if user_input == "exit":
            break

        print("\n助手回答：")
        result = travelHelper.chat(user_input)

        print(result)
