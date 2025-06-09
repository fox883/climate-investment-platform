from services.supabase_client import supabase

# Upsert row (insert or update) in Supabase table
def upsert_row(table_name: str, data: dict):
    return supabase.table(table_name).upsert(data).execute()
