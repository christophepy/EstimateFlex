# src/persistence/scenario_repository.py


from src.models.scenario import Scenario
from src.persistence.database import get_connection
from src.utils.string_utils import normalize_name


class ScenarioRepository:
    """
    CRUD des scénarios.
    """

    @staticmethod
    def _name_exists(
        nom: str,
        exclude_id: int | None = None,
    ) -> bool:
        """
        Vérifie l'unicité d'un nom de scénario
        en ignorant casse et accents.
        """

        normalized = normalize_name(nom)

        for scenario in ScenarioRepository.get_all():

            if exclude_id is not None and scenario.id == exclude_id:
                continue

            if normalize_name(scenario.nom) == normalized:
                return True

        return False

    @staticmethod
    def create(scenario: Scenario) -> int:

        if ScenarioRepository._name_exists(scenario.nom):
            raise ValueError(f"Le scénario '{scenario.nom}' existe déjà.")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO scenarios(
                nom,
                description,
                facteur_productivite,
                facteur_risque,
                facteur_disponibilite,
                actif
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                scenario.nom,
                scenario.description,
                scenario.facteur_productivite,
                scenario.facteur_risque,
                scenario.facteur_disponibilite,
                int(scenario.actif),
            ),
        )

        conn.commit()

        scenario_id = cursor.lastrowid

        conn.close()

        return scenario_id

    @staticmethod
    def get_by_id(
        scenario_id: int,
    ) -> Scenario | None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM scenarios
            WHERE id = ?
            """,
            (scenario_id,),
        )

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return Scenario(
            id=row["id"],
            nom=row["nom"],
            description=row["description"],
            facteur_productivite=row["facteur_productivite"],
            facteur_risque=row["facteur_risque"],
            facteur_disponibilite=row["facteur_disponibilite"],
            actif=bool(row["actif"]),
        )

    @staticmethod
    def get_by_name(
        nom: str,
    ) -> Scenario | None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM scenarios
            WHERE nom = ?
            """,
            (nom,),
        )

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return Scenario(
            id=row["id"],
            nom=row["nom"],
            description=row["description"],
            facteur_productivite=row["facteur_productivite"],
            facteur_risque=row["facteur_risque"],
            facteur_disponibilite=row["facteur_disponibilite"],
            actif=bool(row["actif"]),
        )

    @staticmethod
    def get_all() -> list[Scenario]:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM scenarios
            ORDER BY nom
            """)

        rows = cursor.fetchall()

        conn.close()

        scenarios = []

        for row in rows:

            scenarios.append(
                Scenario(
                    id=row["id"],
                    nom=row["nom"],
                    description=row["description"],
                    facteur_productivite=row["facteur_productivite"],
                    facteur_risque=row["facteur_risque"],
                    facteur_disponibilite=row["facteur_disponibilite"],
                    actif=bool(row["actif"]),
                )
            )

        return scenarios

    @staticmethod
    def update(
        scenario: Scenario,
    ) -> bool:

        if ScenarioRepository._name_exists(
            scenario.nom,
            exclude_id=scenario.id,
        ):
            raise ValueError(f"Le scénario '{scenario.nom}' existe déjà.")
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE scenarios
            SET
                nom = ?,
                description = ?,
                facteur_productivite = ?,
                facteur_risque = ?,
                facteur_disponibilite = ?,
                actif = ?
            WHERE id = ?
            """,
            (
                scenario.nom,
                scenario.description,
                scenario.facteur_productivite,
                scenario.facteur_risque,
                scenario.facteur_disponibilite,
                int(scenario.actif),
                scenario.id,
            ),
        )

        conn.commit()

        updated = cursor.rowcount > 0

        conn.close()

        return updated

    @staticmethod
    def is_used(
        scenario_id: int,
    ) -> bool:

        scenario = ScenarioRepository.get_by_id(scenario_id)

        if scenario is None:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM estimations
            WHERE scenario_nom = ?
            """,
            (scenario.nom,),
        )

        total = cursor.fetchone()["total"]

        conn.close()

        return total > 0

    @staticmethod
    def delete(
        scenario_id: int,
    ) -> bool:

        scenario = ScenarioRepository.get_by_id(scenario_id)

        if scenario is None:
            return False

        if scenario.nom in {
            "Optimiste",
            "Réaliste",
            "Pessimiste",
        }:
            raise ValueError(
                "Les scénarios système ne peuvent pas être supprimés."
            )

        if ScenarioRepository.is_used(scenario_id):
            raise ValueError(
                "Ce scénario est utilisé par une ou plusieurs estimations."
            )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM scenarios
            WHERE id = ?
            """,
            (scenario_id,),
        )

        conn.commit()

        deleted = cursor.rowcount > 0

        conn.close()

        return deleted

    @staticmethod
    def count() -> int:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM scenarios
            """)

        total = cursor.fetchone()["total"]

        conn.close()

        return total
