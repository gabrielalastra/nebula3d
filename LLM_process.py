import os
from openai import OpenAI


def call_chatgpt(title: str, brand: str, material: str, review: str, item_weight: str,
                 color: str, price: str, temperature: float = 0.7,
                 max_tokens: int = 150, model: str = "gpt-3.5-turbo"):
    """
    Interact with the OpenAI GPT model to generate a blog post title and
    content related to 3D printing filament.

    :param title: Title of the filament.
    :param brand: Brand of the filament.
    :param material: Material of the filament.
    :param item_weight: Weight of the filament.
    :param color: Color of the filament.
    :param price: Price of the filament.
    :param temperature: AI response temperature setting.
    :param max_tokens: Maximum number of tokens for generation.
    :param model: Model version of OpenAI GPT.
    :return: Tuple containing generated title and content.
    """
    client = OpenAI()

    # Constructing the message for title generation
    title_message = (
        "Suggest an engaging blog post title related to the following "
        "3D filament: title: {}; brand: {}; material:{}; review:{}; item weight:{}; "
        "color:{}; price:{}. Please be direct in your response without "
        "first-person talk."
    ).format(title, brand, material, review, item_weight, color, price)

    system_message = (
        "You are a writer for a 3D printer filament blog, skilled in explaining, "
        "describing and benchmarking different types of filaments and engaging "
        "the audience."
    )

    response_title = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": title_message}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    # Extracting the response for title
    generated_title = response_title.choices[0].message.content

    # Constructing the message for content generation
    content_message = (
        "Now create an engaging blog post according to the title: {}, "
        "and features such as name: {}; brand: {}; material:{}; review:{}; item weight:{}; "
        "color:{}; price:{}. Please be direct in your response without first-person talk, do not include the title on the text"
    ).format(generated_title, title, brand, material, review, item_weight, color, price)

    response_content = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": content_message}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    # Extracting the response for content
    generated_content = response_content.choices[0].message.content

    return generated_title, generated_content
