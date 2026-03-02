# -*- coding: utf-8 -*-
def post_init(env):
    """Executed automatically right after module installation."""
    cr = env.cr

    # 1️⃣ Enable pgvector extension
    cr.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2️⃣ Add vector column if missing
    cr.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'face_embedding'
                  AND column_name = 'embedding_vec'
            ) THEN
                ALTER TABLE face_embedding ADD COLUMN embedding_vec vector(128);
            END IF;
        END
        $$;
    """)

    # 3️⃣ Fill vector column from JSON (for any existing data)
    cr.execute("""
        UPDATE face_embedding
           SET embedding_vec = (
                CASE
                    WHEN encoding_json IS NULL OR encoding_json = '' THEN NULL
                    ELSE (regexp_replace(encoding_json, '^[\\s]*\\[|\\][\\s]*$', '', 'g'))::text
                END
            )::vector
         WHERE embedding_vec IS NULL
           AND encoding_json IS NOT NULL;
    """)

    # 4️⃣ Create HNSW index (for fast vector search)
    cr.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_indexes WHERE indexname = 'face_embedding_hnsw_idx'
            ) THEN
                CREATE INDEX face_embedding_hnsw_idx
                    ON face_embedding USING hnsw (embedding_vec vector_l2_ops);
            END IF;
        END
        $$;
    """)

    # 5️⃣ Alternative: IVF_FLAT index (uncomment if preferred)
    # cr.execute("""
    #     DO $$
    #     BEGIN
    #         IF NOT EXISTS (
    #             SELECT 1 FROM pg_indexes WHERE indexname = 'face_embedding_ivf_idx'
    #         ) THEN
    #             CREATE INDEX face_embedding_ivf_idx
    #                 ON face_embedding USING ivfflat (embedding_vec vector_l2_ops) WITH (lists = 100);
    #         END IF;
    #     END
    #     $$;
    # """)

    env.cr.commit()  # ensure DDL is persisted
    _logger = getattr(env, "logger", None)
    if _logger:
        _logger.info("✅ pgvector extension and face_embedding index initialized successfully.")


def uninstall_hook(env):
    """Executed when module is uninstalled."""
    cr = env.cr
    # Keep data by default — uncomment if you want cleanup
    # cr.execute("DROP INDEX IF EXISTS face_embedding_hnsw_idx;")
    # cr.execute("ALTER TABLE IF EXISTS face_embedding DROP COLUMN IF EXISTS embedding_vec;")
    cr.commit()
