import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from faker import Faker

# Importe seus modelos aqui
# Substitua 'sua_app' pelo nome real da sua aplicação Django
try:
    from projects.models import Area, Project, ProjectArea, Installment
except ImportError:
    raise CommandError(
        "Não foi possível importar os modelos. Certifique-se de que 'sua_app' "
        "está configurado corretamente e os modelos existem."
    )


class Command(BaseCommand):
    help = "Popula o banco de dados com dados de exemplo usando Faker."

    def add_arguments(self, parser):
        parser.add_argument(
            "--projects",
            type=int,
            default=100,
            help="Número de Projetos a serem criados.",
        )
        parser.add_argument(
            "--installments_per_project",
            type=int,
            default=5,
            help="Número médio de Parcelas por Projeto.",
        )
        parser.add_argument(
            "--project_areas_per_project",
            type=int,
            default=2,
            help="Número médio de Áreas associadas por Projeto.",
        )
        parser.add_argument(
            "--clear-data",
            action="store_true",  # Flag que fica True se passada
            help="Limpa todos os dados de Projetos, ProjectAreas e Installments antes de popular.",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Iniciando população do banco de dados...")
        )

        fake = Faker("pt_BR")  # Usa locale brasileiro

        num_projects = options["projects"]
        avg_installments_per_project = options["installments_per_project"]
        avg_project_areas_per_project = options["project_areas_per_project"]
        clear_data = options["clear_data"]

        # --- Limpar dados existentes (Opcional, útil para recomeçar) ---
        if clear_data:
            self.stdout.write(
                "Limpando dados existentes de Projetos, ProjectAreas e Installments..."
            )
            Installment.objects.all().delete()
            ProjectArea.objects.all().delete()
            Project.objects.all().delete()
            # Não limpamos Area, pois elas vêm da fixture
            self.stdout.write(
                self.style.SUCCESS(
                    "Dados de Projetos, ProjectAreas e Installments limpos."
                )
            )  # --- Fim Limpeza ---

        # # --- 1. Criar Áreas ---
        self.stdout.write(
            "Consultando Áreas existentes no banco de dados (via fixture)..."
        )
        existing_areas = list(Area.objects.all())  # Recupera todas as Áreas

        if not existing_areas:
            raise CommandError(
                "Nenhuma Área encontrada no banco de dados. Certifique-se de que as fixtures "
                "de Áreas foram carregadas corretamente (geralmente durante migrate ou setup)."
            )
        self.stdout.write(
            self.style.SUCCESS(f"{len(existing_areas)} Áreas existentes encontradas.")
        )
        created_areas = (
            existing_areas  # Renomeia para manter a consistência com o código posterior
        )

        # --- 2. Criar Projetos ---
        self.stdout.write(f"Criando {num_projects} Projetos...")
        projects_to_create = []
        status_choices_values = [choice[0] for choice in Project.STATUS_CHOICES]
        current_year = timezone.now().year

        # Define as datas limites como objetos date
        start_date_limit = date(current_year - 2, 1, 1)
        end_date_limit = date(current_year + 1, 12, 31)

        # Gerar processo_sei únicos
        processo_sei_set = set()
        while len(processo_sei_set) < num_projects:
            # Simula o formato ddddd.dddddd/YYYY-MM
            parte1 = str(random.randint(10000, 99999))
            parte2 = str(random.randint(100000, 999999))
            # Ano dentro de um range razoável para processo_sei
            ano_processo = str(random.randint(current_year - 10, current_year + 1))
            mes = str(random.randint(1, 12)).zfill(2)
            processo = f"{parte1}.{parte2}/{ano_processo}-{mes}"
            processo_sei_set.add(processo)

        processo_sei_list = list(processo_sei_set)

        for i in range(num_projects):
            name = fake.catch_phrase()
            description = fake.paragraph(nb_sentences=2)
            # Datas: Projetos que começaram ou vão começar recentemente
            start_date = fake.date_between_dates(
                date_start=start_date_limit, date_end=end_date_limit
            )  # Datas: Projetos com duração variada (3 meses a 2 anos)
            # Gera uma duração aleatória para o projeto (ex: entre 90 dias e 2 anos)
            random_duration_days = random.randint(
                90, 730
            )  # 90 dias (aprox 3 meses) a 730 dias (aprox 2 anos)
            # Calcula a data de fim potencial adicionando a duração à data de início
            potential_end_date = start_date + timedelta(days=random_duration_days)

            # Garante que a data de fim não ultrapasse o limite máximo global
            # Se potential_end_date for depois de end_date_limit, usa end_date_limit
            end_date = min(potential_end_date, end_date_limit)

            # Opcional: Garantir que a data de fim é pelo menos 1 dia depois da data de início
            # (A duração mínima de 90 dias já garante isso, mas é uma salvaguarda)
            if end_date <= start_date:
                end_date = start_date + timedelta(
                    days=1
                )  # Evita projetos com duração zero ou negativa

            total_unb_amount = round(random.uniform(10000.0, 500000.0), 2)

            project = Project(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                total_unb_amount_expected=total_unb_amount,
                # total_fcte_amount_expected é calculado depois (signal)
                # total_compensation_expected/executed/pending/overdue são calculados depois (signal)
                coordinator=fake.name(),
                substitute_coordinator=fake.name(),
                academic_supervisor=fake.name(),
                processo_sei=processo_sei_list[i],
                status=random.choice(status_choices_values),
                nota_dotacao=fake.word() if random.random() > 0.3 else None,  # Opcional
                ptres=fake.word() if random.random() > 0.3 else None,  # Opcional
                ugr=fake.word() if random.random() > 0.3 else None,  # Opcional
                funding_source=(
                    fake.company() if random.random() > 0.3 else None
                ),  # Opcional
                detailed_nature=(
                    str(random.randint(1000, 9999)) if random.random() > 0.3 else None
                ),  # Simula 4 dígitos
                internal_plan=(
                    fake.word() if random.random() > 0.3 else None
                ),  # Opcional
                internal_plan_name=(
                    fake.catch_phrase() if random.random() > 0.3 else None
                ),  # Opcional
            )
            projects_to_create.append(project)

        # Usamos bulk_create dentro de uma transação para garantir atomicidade
        with transaction.atomic():
            created_projects = Project.objects.bulk_create(projects_to_create)

        self.stdout.write(
            self.style.SUCCESS(f"{len(created_projects)} Projetos criados.")
        )

        # Certifique-se que created_areas não está vazio antes de continuar
        # if not created_areas:
        #     self.stdout.write(
        #         self.style.WARNING(
        #             "Nenhuma Área criada. Pulando criação de ProjectArea."
        #         )
        #     )
        #     created_areas = (
        #         []
        #     )  # Garante que a lista está vazia se nenhuma area foi criada
        if not created_projects:
            self.stdout.write(
                self.style.WARNING(
                    "Nenhum Projeto criado. Pulando criação de ProjectArea e Installment."
                )
            )
            created_projects = []  # Garante que a lista está vazia

        # --- 3. Criar ProjectAreas (Many-to-Many) ---
        if created_projects and created_areas:
            self.stdout.write(
                f"Criando ProjectAreas (relacionamentos entre Projetos e Áreas)..."
            )
            project_areas_to_create = []
            for project in created_projects:
                # Associe o projeto a um número aleatório de áreas
                num_areas_for_project = random.randint(
                    1, min(avg_project_areas_per_project * 2, len(created_areas))
                )  # Evita mais áreas do que existem
                # Selecione áreas únicas para este projeto
                areas_for_project = random.sample(created_areas, num_areas_for_project)

                # Distribua os percentuais (simplificado: apenas gera percentual para cada link)
                # Garantir que a soma dos percentuais seja 100% por projeto é mais complexo e pode ser implementado
                # se for um requisito estrito. Para demo, gerar um percentual por link já é útil.
                total_percentage = 100.0  # Vamos tentar distribuir 100%
                remaining_percentage = total_percentage
                for i, area in enumerate(areas_for_project):
                    if i == len(areas_for_project) - 1:
                        percentage = remaining_percentage
                    else:
                        # Garante pelo menos 1%
                        percentage = round(
                            random.uniform(
                                1.0, remaining_percentage / (len(areas_for_project) - i)
                            ),
                            2,
                        )
                    percentage = min(
                        percentage, remaining_percentage
                    )  # Evita ultrapassar o restante
                    percentage = max(percentage, 0.0)  # Garante que não é negativo
                    remaining_percentage -= percentage

                    project_areas_to_create.append(
                        ProjectArea(
                            project=project,
                            area=area,
                            percentage=Decimal(
                                str(percentage)
                            ),  # DecimalField requer Decimal object
                        )
                    )

            # Usamos bulk_create dentro de uma transação
            with transaction.atomic():
                created_project_areas = ProjectArea.objects.bulk_create(
                    project_areas_to_create, ignore_conflicts=True
                )  # ignore_conflicts para o unique_together

            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(created_project_areas)} ProjectAreas criadas."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Não foi possível criar ProjectAreas. Certifique-se de que Projetos e Áreas foram criados."
                )
            )

        # --- 4. Criar Parcelas (Installments) ---
        if created_projects:
            self.stdout.write(f"Criando Parcelas para os Projetos...")
            installments_to_create = []
            # Não precisamos mais da lista de valores de status aqui, pois vamos determiná-lo.
            # installment_status_values = [choice[0] for choice in Installment.STATUS_CHOICES]

            for project in created_projects:
                # Número aleatório de parcelas por projeto (dentro de um range)
                num_installments = random.randint(
                    max(1, avg_installments_per_project - 2),
                    avg_installments_per_project + 3,
                )  # Garante pelo menos 1

                for i in range(num_installments):
                    # Gera datas de parcelas dentro do período do projeto
                    # estimated_date pode ser no passado, presente ou futuro
                    estimated_date = fake.date_between_dates(
                        date_start=project.start_date, date_end=project.end_date
                    )

                    effective_date = None
                    status = "Pendente"  # Status padrão

                    # *** Lógica Ajustada para Status e effective_date ***

                    # Determine o status com base na estimated_date em relação à data atual
                    if estimated_date > timezone.now().date():
                        # Se a data estimada está no futuro, o status é sempre Pendente
                        status = "Pendente"
                        effective_date = (
                            None  # Não tem data efetiva para parcela futura pendente
                        )
                    else:
                        # Se a data estimada está no passado ou presente
                        # Pode ser Quitada ou Atrasada (ou Pendente, se houver uma regra de negócio para isso)
                        # Vamos randomizar entre Quitada e Atrasada para parcelas passadas/presentes
                        status = random.choice(["Quitada", "Atrasada"])

                        if status == "Quitada":
                            # Data efetiva deve ser entre a data estimada e a data atual (inclusive)
                            # O intervalo [estimated_date, timezone.now().date()] é VÁLIDO aqui porque estimated_date <= hoje
                            effective_date = fake.date_between_dates(
                                date_start=estimated_date,
                                date_end=timezone.now().date(),
                            )
                        elif status == "Atrasada":
                            # Para status Atrasada, effective_date é None
                            effective_date = None

                    # *** Fim da Lógica Ajustada ***

                    # Montante da parcela (simplesmente distribui o total esperado, com variação)
                    amount = round(
                        project.total_unb_amount_expected * random.uniform(0.05, 0.3), 2
                    )

                    installments_to_create.append(
                        Installment(
                            project=project,
                            amount=amount,
                            estimated_date=estimated_date,
                            effective_date=effective_date,
                            observation=(
                                fake.sentence() if random.random() > 0.5 else None
                            ),  # Opcional
                            destination=(
                                fake.company() if random.random() > 0.4 else None
                            ),  # Opcional
                            status=status,  # Usa o status (agora determinado)
                        )
                    )  # Usamos bulk_create dentro de uma transação

            with transaction.atomic():
                created_installments = Installment.objects.bulk_create(
                    installments_to_create
                )

            self.stdout.write(
                self.style.SUCCESS(f"{len(created_installments)} Parcelas criadas.")
            )

            # --- 5. Recalcular Totais dos Projetos (Necessário porque bulk_create não dispara sinais) ---
            self.stdout.write("Recalculando totais de compensação para os Projetos...")
            # Precisamos recuperar os projetos novamente para garantir que estão atualizados
            # ou apenas chamar o método calculate_compensation_totals() nos objetos que já temos.
            # Chamar o método diretamente nos objetos criados é mais eficiente.
            # O método calculate_compensation_totals() já salva o objeto Project.
            for project in created_projects:
                project.calculate_compensation_totals()
            self.stdout.write(self.style.SUCCESS("Totais de compensação recalculados."))

        else:
            self.stdout.write(
                self.style.WARNING(
                    "Não foi possível criar Parcelas. Certifique-se de que Projetos foram criados."
                )
            )

        self.stdout.write(self.style.SUCCESS("População do banco de dados concluída!"))
