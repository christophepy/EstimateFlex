# src/persistence/estimation_repository.py

from datetime import datetime

from src.models.estimation_result import (
    EstimationResult,
)
from src.persistence.database import (
    get_connection,
)


class EstimationRepository:

    def save(
        self,
        estimation: EstimationResult,
    ) -> None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO estimations(
                estimation_nom,
                project_nom,
                profile_nom,
                scenario_nom,
                estimated_hours,
                estimated_days,
                estimated_cost,
                risk_factor,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                estimation.estimation_nom,
                estimation.project_nom,
                estimation.profile_nom,
                estimation.scenario_nom,
                estimation.estimated_hours,
                estimation.estimated_days,
                estimation.estimated_cost,
                estimation.risk_factor,
                estimation.created_at,
            ),
        )

        conn.commit()
        conn.close()

    def get_all(
        self,
    ) -> list[EstimationResult]:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM estimations
            ORDER BY created_at DESC
            """)

        rows = cursor.fetchall()

        conn.close()

        estimations = []

        for row in rows:

            estimations.append(
                EstimationResult(
                    id=row["id"],
                    estimation_nom=row["estimation_nom"] or "",
                    project_nom=row["project_nom"],
                    profile_nom=row["profile_nom"],
                    scenario_nom=row["scenario_nom"],
                    estimated_hours=row["estimated_hours"],
                    estimated_days=row["estimated_days"],
                    estimated_cost=row["estimated_cost"],
                    risk_factor=row["risk_factor"],
                    created_at=row["created_at"],
                )
            )

        return estimations

    def get_estimation(
        self,
        estimation_id: int,
    ) -> EstimationResult | None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM estimations
            WHERE id = ?
            """,
            (estimation_id,),
        )

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return EstimationResult(
            id=row["id"],
            estimation_nom=row["estimation_nom"] or "",
            project_nom=row["project_nom"],
            profile_nom=row["profile_nom"],
            scenario_nom=row["scenario_nom"],
            estimated_hours=row["estimated_hours"],
            estimated_days=row["estimated_days"],
            estimated_cost=row["estimated_cost"],
            risk_factor=row["risk_factor"],
            created_at=row["created_at"],
        )

    def delete_estimation(
        self,
        estimation_id: int,
    ) -> None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM estimations
            WHERE id = ?
            """,
            (estimation_id,),
        )

        conn.commit()
        conn.close()

    def rename_estimation(
        self,
        estimation_id: int,
        new_name: str,
    ) -> None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE estimations
            SET estimation_nom = ?
            WHERE id = ?
            """,
            (
                new_name,
                estimation_id,
            ),
        )

        conn.commit()
        conn.close()

    def duplicate_estimation(
        self,
        estimation_id: int,
    ) -> int | None:

        estimation = self.get_estimation(estimation_id)

        if estimation is None:
            return None

        copy_name = f"{estimation.estimation_nom}_COPIE"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO estimations(
                estimation_nom,
                project_nom,
                profile_nom,
                scenario_nom,
                estimated_hours,
                estimated_days,
                estimated_cost,
                risk_factor,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                copy_name,
                estimation.project_nom,
                estimation.profile_nom,
                estimation.scenario_nom,
                estimation.estimated_hours,
                estimation.estimated_days,
                estimation.estimated_cost,
                estimation.risk_factor,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        new_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return new_id

    def count(self) -> int:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM estimations
            """)

        total = cursor.fetchone()["total"]

        conn.close()

        return total
