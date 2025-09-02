from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Force clean database setup - drops all tables and recreates from scratch'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR('⚠️ Este comando irá APAGAR TODOS OS DADOS!')
            )
            self.stdout.write(
                'Para confirmar, execute: python manage.py force_clean_db --confirm'
            )
            return

        self.stdout.write(
            self.style.WARNING('🚨 ATENÇÃO: Limpando banco de dados completamente...')
        )
        
        try:
            # Obter todas as tabelas
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                """)
                tables = [row[0] for row in cursor.fetchall()]
            
            if tables:
                self.stdout.write(f'🗑️ Removendo {len(tables)} tabelas...')
                
                # Desabilitar verificação de chaves estrangeiras
                with connection.cursor() as cursor:
                    cursor.execute('SET foreign_key_checks = 0;')
                    
                    # Deletar todas as tabelas
                    for table in tables:
                        cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                        self.stdout.write(f'  ❌ Removida: {table}')
                    
                    cursor.execute('SET foreign_key_checks = 1;')
            
            self.stdout.write(
                self.style.SUCCESS('✅ Banco limpo com sucesso!')
            )
            
            # Recriar estrutura
            self.stdout.write('🔄 Recriando estrutura do banco...')
            call_command('makemigrations', verbosity=1)
            call_command('migrate', verbosity=1)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Banco recriado com sucesso!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao limpar banco: {e}')
            )
