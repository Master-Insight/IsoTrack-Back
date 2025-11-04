# app/modules/routes.py
from fastapi import FastAPI

from app.libraries.utils.response_builder import ResponseBuilder

from app.modules.companies.api.routes import router as companies_router
from app.modules.users.api.routes import router as users_router
from app.modules.product_photos.api.routes import router as product_photos_router
from app.modules.products.api.routes import router as products_router
from app.modules.clients.api.routes import router as clients_router

from app.modules.deals.api.routes import router as deals_router
from app.modules.deal_notes.api.routes import router as deal_notes_router
from app.modules.quotations.api.routes import router as quotations_router

from app.modules.analytics.api.routes import router as analytics_router
from app.modules.test.routes import router as test_router


def register_routes(app: FastAPI):
    # --- Ruta base ---
    @app.get("/")
    def read_root():
        return ResponseBuilder.success("DealerApp API funcionando correctamente 🚗")

    # --- Rutas de módulos Primarios ---
    app.include_router(companies_router, prefix="/companies", tags=["Companies"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(products_router, prefix="/products", tags=["Products"])
    app.include_router(
        product_photos_router, prefix="/products", tags=["Product Photos"]
    )
    app.include_router(clients_router, prefix="/clients", tags=["Clients"])

    # --- Rutas de módulos Combinados ---
    app.include_router(deals_router, prefix="/deals", tags=["Deals"])
    app.include_router(deal_notes_router, prefix="/deals", tags=["Deal Notes"])
    app.include_router(quotations_router, prefix="/quotations", tags=["Quotations"])

    # --- Rutas de módulos Adicionales ---
    app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])

    app.include_router(test_router, prefix="/test")
