"""schema_v2

Revision ID: 002_schema_v2
Revises: 001_initial
Create Date: 2026-03-10 13:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_schema_v2'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Update Users Table
    op.execute("DO $$ BEGIN CREATE TYPE userrole AS ENUM ('ADMIN', 'USER'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.add_column('users', sa.Column('role', sa.Enum(
        'ADMIN', 'USER', name='userrole'), server_default='USER', nullable=False))

    op.alter_column('users', 'hashed_password',
                    new_column_name='password_hash')
    op.alter_column('users', 'email', type_=sa.String(length=255))

    # Remove username column
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'username')
    # Remove is_active column
    op.drop_column('users', 'is_active')
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_pw = pwd_context.hash("admin")
    op.execute(f"INSERT INTO users (id, email, password_hash, role, created_at, updated_at) "
               f"VALUES ('123e4567-e89b-12d3-a456-426614174001', 'admin@example.com', '{hashed_pw}', 'ADMIN', now(), now())")
    # 2. Update Books Table
    # Drop old owner_id foreign key constraint and column
    op.drop_constraint('books_owner_id_fkey', 'books', type_='foreignkey')
    op.drop_column('books', 'owner_id')

    # Drop old columns
    op.drop_column('books', 'year')
    op.drop_column('books', 'price')
    op.drop_column('books', 'is_available')

    # Alter existing columns
    op.alter_column('books', 'title', type_=sa.String(length=100))
    op.alter_column('books', 'author', type_=sa.String(length=100))
    op.alter_column('books', 'description', type_=sa.Text())

    # Add new columns
    op.add_column('books', sa.Column(
        'isbn', sa.String(length=20), nullable=True))
    op.add_column('books', sa.Column(
        'publisher', sa.String(length=100), nullable=True))
    op.add_column('books', sa.Column('publish_date', sa.Date(), nullable=True))

    # 3. Create UserBook Table (M2M)
    # op.execute("DO $$ BEGIN CREATE TYPE bookstatus AS ENUM ('READING', 'COMPLETED', 'PLAN_TO_READ', 'DROPPED'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    op.create_table('user_books',
                    sa.Column('user_id', sa.UUID(), nullable=False),
                    sa.Column('book_id', sa.UUID(), nullable=False),
                    sa.Column('status', sa.Enum('READING', 'COMPLETED',
                                                'PLAN_TO_READ', 'DROPPED', name='bookstatus'), nullable=False),
                    sa.Column('added_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['book_id'], ['books.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.execute("INSERT INTO books (id, title, author, genre, description, isbn, publisher, publish_date, created_at, updated_at) "
               "VALUES (gen_random_uuid(), 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 'A novel set in the Roaring Twenties.', '978-5-389-01666-8', 'Scribner', '1925-04-10', now(), now())"
               ", (gen_random_uuid(), 'To Kill a Mockingbird', 'Harper Lee', 'Classic', 'A novel about racial injustice in the Deep South.', '978-5-17-085350-2', 'J.B. Lippincott & Co.', '1960-07-11', now(), now())"
               ", (gen_random_uuid(), '1984', 'George Orwell', 'Dystopian', 'A dystopian novel set in a totalitarian society.', '978-5-699-96831-2', 'Secker & Warburg', '1949-06-08', now(), now())"
               ", (gen_random_uuid(), 'Neuromancer', 'William Gibson', 'Science Fiction', 'A novel that coined the term cyberspace.', '978-5-699-90603-1', 'Ace Books', '1984-07-01', now(), now())")


def downgrade() -> None:
    pass
