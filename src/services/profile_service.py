# Gestion complète des profils
"""
Profile Service
EstimateFlex v1.0
"""

from __future__ import annotations

from dataclasses import replace

from src.models.user_profile import UserProfile
from src.persistence.profile_repository import ProfileRepository


class ProfileService:
    """
    Service métier de gestion des profils utilisateurs.
    """

    def __init__(self, repository: ProfileRepository | None = None):
        self.repository = repository or ProfileRepository()

    # =========================================================
    # CRUD
    # =========================================================

    def create_profile(self, profile: UserProfile) -> int:
        """
        Crée un nouveau profil.
        """

        if not profile.nom.strip():
            raise ValueError("Le nom du profil est obligatoire.")

        existing = self.repository.get_by_name(profile.nom)

        if existing:
            raise ValueError(f"Le profil '{profile.nom}' existe déjà.")

        return self.repository.create(profile)

    def update_profile(self, profile: UserProfile) -> bool:
        """
        Met à jour un profil existant.
        """

        if profile.id is None:
            raise ValueError("Impossible de mettre à jour un profil sans identifiant.")

        existing = self.repository.get_by_id(profile.id)

        if not existing:
            raise ValueError(f"Profil introuvable : {profile.id}")

        return self.repository.update(profile)

    def delete_profile(self, profile_id: int) -> bool:
        """
        Supprime un profil.
        """

        existing = self.repository.get_by_id(profile_id)

        if not existing:
            raise ValueError(f"Profil introuvable : {profile_id}")

        return self.repository.delete(profile_id)

    # =========================================================
    # Lecture
    # =========================================================

    def get_profile(self, profile_id: int) -> UserProfile | None:
        """
        Retourne un profil par son ID.
        """
        return self.repository.get_by_id(profile_id)

    def get_profile_by_nom(self, nom: str) -> UserProfile | None:
        """
        Recherche un profil par son nom.
        """
        return self.repository.get_by_name(nom)

    def get_all_profiles(self) -> list[UserProfile]:
        """
        Retourne tous les profils.
        """
        return self.repository.get_all()

    # =========================================================
    # Gestion profil par défaut
    # =========================================================

    def get_default_profile(self) -> UserProfile | None:
        profiles = self.repository.get_all()

        if not profiles:
            return None

        return profiles[0]

    def set_default_profile(
        self,
        profile_id: int,
    ) -> bool:
        """
        Fonction conservée pour compatibilité.
        V1 : aucun profil par défaut configurable.
        """
        return True

    # =========================================================
    # Validation
    # =========================================================

    def validate_profile(self, profile: UserProfile) -> tuple[bool, list[str]]:
        """
        Vérifie qu'un profil est valide.
        """

        errors = []

        if not profile.nom.strip():
            errors.append("Le nom du profil est obligatoire.")

        if hasattr(profile, "daily_rate") and profile.daily_rate < 0:
            errors.append("Le taux journalier doit être positif.")

        if hasattr(profile, "productivity") and profile.productivity <= 0:
            errors.append("La productivité doit être supérieure à zéro.")

        if hasattr(profile, "risk_factor") and profile.risk_factor < 0:
            errors.append("Le facteur de risque est invalide.")

        return len(errors) == 0, errors

    # =========================================================
    # Fonctions métier
    # =========================================================

    def duplicate_profile(self, profile_id: int, new_nom: str) -> int:
        """
        Duplique un profil existant.
        """

        source = self.repository.get_by_id(profile_id)

        if not source:
            raise ValueError(f"Profil introuvable : {profile_id}")

        duplicated = replace(source, id=None, nom=new_nom)

        return self.create_profile(duplicated)

    def count_profiles(self) -> int:
        """
        Nombre total de profils.
        """
        return len(self.repository.get_all())
