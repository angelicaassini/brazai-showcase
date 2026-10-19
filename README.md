<h1 align="center">🍔 BrazAI</h1>

<p align="center">
  <b>SaaS de delivery multi-tenant para restaurantes</b><br/>
  <i>Multi-tenant delivery SaaS for restaurants — pizzerias, burger joints & more</i><br/>
  <sub>🚧 Atendimento por <b>IA no WhatsApp</b> — em construção · <i>WhatsApp AI agent — work in progress</i></sub>
</p>

<p align="center">
  <a href="https://brazai.vercel.app"><b>▶ Demo ao vivo · Painel (entre como visitante)</b></a>
  &nbsp;·&nbsp;
  <a href="https://brazai.vercel.app/cardapio/atelier-gastronomico"><b>📱 Cardápio do cliente</b></a><br/>
  <i>Live demo · Owner panel (log in as a visitor) &nbsp;·&nbsp; Customer menu</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/DRF-A30000?style=flat&logo=django&logoColor=white" alt="DRF"/>
  <img src="https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB" alt="React"/>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/Material%20UI-007FFF?style=flat&logo=mui&logoColor=white" alt="MUI"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/WhatsApp%20AI-em%20breve-25D366?style=flat&logo=whatsapp&logoColor=white" alt="WhatsApp AI — em breve"/>
</p>

---

## ✨ Visão geral · Overview

O **BrazAI** é um sistema de delivery onde **cada restaurante é um _tenant_ com dados
totalmente isolados** — cardápio, pedidos e configurações próprios. O dono acompanha os
pedidos em tempo real num painel simples, e o cliente pede pelo **cardápio web** (com
checkout e acompanhamento do pedido). Um **agente de IA no WhatsApp** — que monta o pedido
sozinho — está **em construção** 🚧.

*Each restaurant is a fully isolated tenant with its own menu, orders and settings. Owners
track orders in real time; customers order through a web menu (checkout + live tracking).
A WhatsApp AI ordering agent is in progress.*

> 📌 Este é o **repositório-vitrine** do projeto. O código-fonte completo é **privado**
> (produto comercial — as licenças de uso são vendidas). Aqui ficam a **demo ao vivo**,
> **capturas de tela**, a **arquitetura** e **trechos curados** do código.
>
> *This is the project's **showcase repository**. The full source code is **private**
> (commercial product — usage licences are sold). Here you'll find the **live demo**,
> **screenshots**, the **architecture** and **curated code excerpts**.*

---

## 🧱 Stack

| Camada · Layer | Tecnologias · Technologies |
|---|---|
| **Backend** | Python · Django · Django REST Framework · JWT (SimpleJWT) |
| **Frontend** | React · TypeScript · Vite · Material UI · React Query · Zustand |
| **IA / WhatsApp** 🚧 | Meta WhatsApp Cloud API · LLM plugável (Groq / Gemini) com _function calling_ — **em construção**<br/>*Meta WhatsApp Cloud API · pluggable LLM (Groq / Gemini) with function calling — **work in progress*** |
| **Banco · Database** | PostgreSQL |
| **Qualidade · Quality** | 105 testes de backend · checagem de tipos (`tsc`) · Vitest<br/>*105 backend tests · type checking (`tsc`) · Vitest* |
| **Deploy** | Vercel (front) · Render (API) · Supabase (DB) |

---

## 🏛️ Arquitetura & destaques · Architecture & highlights

- **Multi-tenancy** (_shared-schema_): coluna `tenant` em todas as tabelas + um
  `TenantFilterMixin` que **isola os dados de cada restaurante automaticamente**, sem
  repetir filtros em cada view.<br/>
  *A `tenant` column on every table + a `TenantFilterMixin` that **isolates each
  restaurant's data automatically**, with no filters repeated in every view.*
- **Máquina de estados dos pedidos**: `RECEBIDO → ACEITO → EM_PREPARO → A_CAMINHO →
  CONCLUÍDO` (+ `CANCELADO`), com transições validadas no backend.<br/>
  ***Order state machine**: received → accepted → preparing → on the way → completed
  (+ cancelled), with transitions validated on the backend.*
- **Pizza meio a meio**: dois sabores num pedido, com preço pelo **sabor mais caro** ou
  pela **média** (configurável por restaurante) — validado e "congelado" no item.<br/>
  ***Half-and-half pizza**: two flavours in one item, priced by the **most expensive
  flavour** or the **average** (configurable per restaurant) — validated and "frozen" on the
  order item.*
- **Agente de IA no WhatsApp** 🚧 _(em construção)_: recebe mensagens por webhook, monta o
  pedido com _function calling_ e provider de LLM **plugável** (Groq / Gemini / mock).<br/>
  ***WhatsApp AI agent** 🚧 (work in progress): receives messages via webhook, builds the
  order with function calling and a **pluggable** LLM provider (Groq / Gemini / mock).*
- **Modo visitante**: middleware de **somente-leitura** deixa visitantes
  explorarem o app por dentro sem alterar os dados.<br/>
  ***Visitor mode**: a **read-only** middleware lets visitors explore the app from the
  inside without changing any data.*
- **Padrão Selectors/Services**: regra de negócio separada das views → testável sem subir
  um request HTTP.<br/>
  ***Selectors/Services pattern**: business rules kept out of the views → testable without
  an HTTP request.*
- **Autenticação JWT** com papéis (`SAAS_ADMIN` / `BUSINESS_ADMIN` / `OPERATOR`); datas em
  **UTC** no banco.<br/>
  ***JWT authentication** with roles (`SAAS_ADMIN` / `BUSINESS_ADMIN` / `OPERATOR`);
  **UTC** datetimes in the database.*

---

## 🔎 Trechos de código · Code highlights

> Amostras **curadas** (não-rodáveis) que mostram o estilo de código e as decisões de
> arquitetura. Arquivos completos em [`snippets/`](snippets/).
>
> *Curated (non-runnable) samples showing the coding style and architectural decisions. Full
> files in [`snippets/`](snippets/).*

### 1. Isolamento multi-tenant · Multi-tenant isolation — `TenantFilterMixin`

Toda ViewSet que herda este mixin filtra os dados pelo restaurante do usuário logado e
injeta o `tenant` ao criar registros. **Isolamento por construção.**

*Every ViewSet that inherits this mixin filters data by the logged-in user's restaurant and
injects the `tenant` when creating records. **Isolation by construction.***

```python
class TenantFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user, 'tenant_id', None):
            return queryset.filter(tenant=user.tenant)
        return queryset.none()

    def perform_create(self, serializer):
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant is None:
            raise PermissionDenied('Sua conta não está vinculada a um restaurante.')
        serializer.save(tenant=tenant)
```

### 2. Modo visitante · Visitor mode — `ReadOnlyVisitorMiddleware`

A trava por trás do "Entrar como visitante": o visitante VÊ tudo, mas escritas são barradas
no middleware (vale para TODAS as rotas, mesmo as com `permission_classes` próprias).

*The lock behind "Log in as a visitor": the visitor SEES everything, but writes are blocked
in the middleware (it applies to ALL routes, even those with their own `permission_classes`).*

```python
class ReadOnlyVisitorMiddleware:
    def __call__(self, request):
        if (request.method not in SAFE_METHODS
                and request.path.startswith('/api/')
                and request.path not in _EXEMPT_PATHS):
            result = self._jwt.authenticate(request)
            if result is not None and getattr(result[0], 'is_readonly', False):
                return JsonResponse({'detail': _MESSAGE}, status=403)
        return self.get_response(request)
```

### 3. Regra do meio a meio + teste · Half-and-half rule + test

Preço pelo sabor mais caro (MAX) ou pela média (AVG), e um teste que prova as duas regras.

*Price by the most expensive flavour (MAX) or by the average (AVG), and a test that proves the
rules.*

```python
def half_and_half_price(settings_obj, price_a, price_b):
    if settings_obj.half_and_half_pricing == settings_obj.AVG:
        return ((price_a + price_b) / Decimal('2')).quantize(CENT, rounding=ROUND_HALF_UP)
    return max(price_a, price_b)

def test_half_and_half_uses_max_price(self):
    order = services.place_order(..., items=[self._pizza_item(second_product=str(self.pizza2.id))])
    self.assertEqual(order.items.first().unit_price, Decimal('50.00'))   # o sabor mais caro
```

---

## 📫 Contato · Contact

- 📧 [assini.angelica@gmail.com](mailto:assini.angelica@gmail.com)

---

## 🖥️ Telas · Screenshots

**Cardápio do cliente** — foto, descrição, restrições e busca por item/ingrediente<br/>
***Customer menu** — photo, description, dietary restrictions and search by item/ingredient*

<p><img src="assets/01-cardapio.png" alt="Cardápio do cliente" width="340"/></p>

**A jornada do cliente · The customer journey**

<table>
  <tr>
    <td width="50%" valign="top" align="center"><b>Escolha do prato + adicionais (ponto da carne)</b><br/><i>Choosing the dish + add-ons (meat doneness)</i><br/><img src="assets/02-produto-ponto.png" alt="Ponto da carne" width="320"/></td>
    <td width="50%" valign="top" align="center"><b>Pizza meio a meio</b><br/><i>Half-and-half pizza</i><br/><img src="assets/03-meio-a-meio.png" alt="Pizza meio a meio" width="320"/></td>
  </tr>
  <tr>
    <td valign="top" align="center"><b>Carrinho</b><br/><i>Cart</i><br/><img src="assets/04-carrinho.png" alt="Carrinho" width="320"/></td>
    <td valign="top" align="center"><b>Checkout</b><br/><img src="assets/05-checkout.png" alt="Checkout" width="320"/></td>
  </tr>
</table>

**Acompanhamento do pedido em tempo real · Live order tracking**

<p><img src="assets/06-acompanhamento.png" alt="Acompanhamento do pedido" width="300"/></p>

**Acesso & painel do restaurante · Login & owner panel** — entre em 1 clique com **"Entrar como visitante"** · *log in with 1 click via **"Log in as a visitor"***

<table>
  <tr>
    <td width="50%" valign="top" align="center"><b>Login (modo visitante)</b><br/><i>Login (visitor mode)</i><br/><img src="assets/08-login.png" alt="Login" width="320"/></td>
    <td width="50%" valign="top" align="center"><b>Esteira de pedidos (tempo real)</b><br/><i>Order pipeline (real time)</i><br/><img src="assets/07-painel-pedidos.png" alt="Painel de pedidos" width="320"/></td>
  </tr>
</table>
