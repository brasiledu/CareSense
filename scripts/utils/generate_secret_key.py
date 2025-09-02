#!/usr/bin/env python3
"""
Script para gerar uma SECRET_KEY segura para Django
Use isso para gerar a SECRET_KEY no Render
"""

from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    print("SECRET_KEY segura para Django:")
    print(get_random_secret_key())
    print("\nCopie esta chave e use como variável de ambiente SECRET_KEY no Render")
