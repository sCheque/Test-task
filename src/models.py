from sqlalchemy import Integer, String, Boolean, Float, ForeignKey, MetaData
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


metadata = MetaData()


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"


    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    on_sale: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text('now()'),
        nullable=False
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer,primary_key=True ,nullable=False)
    name: Mapped[str] = mapped_column(String)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


