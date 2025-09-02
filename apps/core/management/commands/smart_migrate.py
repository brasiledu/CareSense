from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Resolve migration conflicts automatically for production deployment'

    def handle(self, *args, **options):
        """
        Comando inteligente que resolve conflitos de migração automaticamente
        """
        self.stdout.write('🔧 Resolvendo conflitos de migração...')
        
        # Verificar se é PostgreSQL (produção) ou SQLite
        db_engine = settings.DATABASES['default']['ENGINE']
        
        if 'postgresql' in db_engine:
            self.stdout.write('🐘 PostgreSQL detectado - Executando migrações normais')
            try:
                call_command('migrate', verbosity=1)
                self.stdout.write(
                    self.style.SUCCESS('✅ Migrações executadas com sucesso!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro nas migrações: {e}')
                )
                raise
        
        elif 'sqlite3' in db_engine:
            self.stdout.write('🔧 SQLite detectado - Modo de compatibilidade')
            
            # Para SQLite, tentar diferentes estratégias
            try:
                # Primeira tentativa: migração normal
                call_command('migrate', verbosity=1)
                self.stdout.write(
                    self.style.SUCCESS('✅ Migrações SQLite executadas com sucesso!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Migração normal falhou: {e}')
                )
                
                try:
                    # Segunda tentativa: fake inicial
                    self.stdout.write('🔄 Tentando migração com --fake-initial...')
                    call_command('migrate', fake_initial=True, verbosity=1)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Migrações com fake-initial executadas!')
                    )
                except Exception as e2:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️ Fake-initial falhou: {e2}')
                    )
                    
                    try:
                        # Terceira tentativa: syncdb
                        self.stdout.write('🔄 Tentando com --run-syncdb...')
                        call_command('migrate', run_syncdb=True, verbosity=1)
                        self.stdout.write(
                            self.style.SUCCESS('✅ Migrações com syncdb executadas!')
                        )
                    except Exception as e3:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Todas as tentativas falharam: {e3}')
                        )
                        raise
        
        else:
            self.stdout.write(f'🤔 Banco desconhecido: {db_engine}')
            call_command('migrate', verbosity=1)
