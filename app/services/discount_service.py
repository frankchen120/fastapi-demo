from app.schemas.discount import Discount, DiscountResponse

def calculate_discount(data: Discount) -> DiscountResponse:
    final_price = data.price * (1 - data.discount)
    return DiscountResponse(
        name= data.name,
        final_price= final_price
    )
        