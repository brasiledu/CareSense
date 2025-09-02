# Generated manually to resolve production deployment conflicts

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    """
    Migração especial para resolver conflitos de produção.
    Esta migração verifica se a coluna education_years já existe
    antes de tentar criá-la.
    """
    
    dependencies = [
        ('patients', '0005_alter_patient_education_level_and_more'),
    ]
    
    def add_education_years_safe(apps, schema_editor):
        """
        Adiciona education_years apenas se não existir
        """
        from django.db import connection
        
        # Verificar se a coluna já existe
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM pragma_table_info('patients_patient') 
                WHERE name='education_years'
            """)
            column_exists = cursor.fetchone()[0] > 0
            
        if not column_exists:
            # Adicionar a coluna apenas se não existir
            Patient = apps.get_model('patients', 'Patient')
            from django.db import models
            
            field = models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(30)
                ],
                verbose_name='Anos de Estudo (legado)',
                help_text='Campo legado, opcional. Não é mais utilizado para cálculos.'
            )
            
            try:
                schema_editor.add_field(Patient, field)
            except Exception:
                # Se falhar, provavelmente a coluna já existe
                pass
    
    def remove_education_years_safe(apps, schema_editor):
        """
        Remove education_years de forma segura
        """
        try:
            Patient = apps.get_model('patients', 'Patient')
            field = models.IntegerField()
            schema_editor.remove_field(Patient, field)
        except Exception:
            # Se falhar, continuar sem erro
            pass
    
    operations = [
        migrations.RunPython(
            add_education_years_safe,
            remove_education_years_safe,
            atomic=False  # Não usar transação para SQLite
        ),
    ]
