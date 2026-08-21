"""
BrazAI — Regra de preço do "meio a meio" de pizza + teste (trecho curado).

Uma pizza pode ser meio de um sabor, meio de outro. O preço segue a configuração
do restaurante: o do sabor MAIS CARO (MAX) ou a MÉDIA dos dois (AVG). O valor é
validado e "congelado" no item no momento do pedido (não muda se o preço mudar
depois). Amostra curada (não-rodável).
"""
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal('0.01')


def half_and_half_price(settings_obj, price_a, price_b):
    """MAX = cobra o sabor mais caro; AVG = média dos dois sabores."""
    if settings_obj.half_and_half_pricing == settings_obj.AVG:
        return ((price_a + price_b) / Decimal('2')).quantize(CENT, rounding=ROUND_HALF_UP)
    return max(price_a, price_b)


def build_half_and_half(product, second, settings_obj):
    """Valida os dois sabores e devolve o preço unitário do item meio a meio."""
    if not product.allow_half_and_half:
        raise ValidationError(f'"{product.name}" não aceita meio-a-meio.')
    if not second.allow_half_and_half:
        raise ValidationError(f'"{second.name}" não pode ser usado como sabor.')
    return half_and_half_price(settings_obj, product.price, second.price)


# --- Testes (prova de qualidade) ------------------------------------------
def test_half_and_half_uses_max_price(self):
    order = services.place_order(
        tenant=self.tenant, customer_name='Ana', fulfillment_type=Order.PICKUP,
        items=[self._pizza_item(second_product=str(self.pizza2.id))],
    )
    item = order.items.first()
    self.assertTrue(item.is_half_and_half)
    self.assertEqual(item.unit_price, Decimal('50.00'))   # o sabor mais caro

def test_half_and_half_average_when_configured(self):
    s = get_settings(self.tenant)
    s.half_and_half_pricing = s.AVG
    s.save(update_fields=['half_and_half_pricing'])
    order = services.place_order(
        tenant=self.tenant, customer_name='Ana', fulfillment_type=Order.PICKUP,
        items=[self._pizza_item(second_product=str(self.pizza2.id))],
    )
    self.assertEqual(order.items.first().unit_price, Decimal('47.50'))  # (45+50)/2
