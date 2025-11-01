import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# from weather_agent import result_weather

dotenv.load_dotenv()


def clothes_recommender(weather):
    """
    穿搭推荐
    :param weather:
    :return:
    """

    llm = ChatOpenAI(
        model = "gpt-4o-mini"
    )

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的穿搭顾问，根据天气信息为用户提供合适的穿搭建议。

        请根据以下天气信息，给出详细、实用的穿搭推荐：
        - 考虑温度、湿度、风速、天气状况
        - 推荐具体的服装类型和材质
        - 给出搭配建议和注意事项
        - 语气亲切专业、语言简短精炼

        输出格式：
        👕 穿搭推荐：
        [具体的推荐内容]

        💡 温馨提示：
        [注意事项]"""),
        ("human", "天气信息：\n{weather}")
    ])

    chain = prompt_template | llm

    response = chain.invoke({"weather":weather})
    return response.content



# if __name__ == '__main__':
#     weather = result_weather['output']
#     recommender = clothes_recommender(weather)
#     print(recommender)