# ← signup(), login(), logout() functions#

from .supabase_client import supabase  # 👈 relative import

def login(email, password):
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

def signup(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })
