# Architecture Report

> Source analysée : `src`

## Vue d'ensemble

- Modules : **58**
- Classes : **52**
- Fonctions top-level : **29**
- Dataclasses : **12**
- Enums : **1**
- ABC / interfaces : **0**
- Dépendances circulaires : **0**

## Architecture des modules

```mermaid
flowchart LR
    [""]
    config["config"]
    config_paths["config.paths"]
    core["core"]
    core_constants["core.constants"]
    core_estimation["core.estimation"]
    core_estimation_cost_engine["core.estimation.cost_engine"]
    core_estimation_duration_engine["core.estimation.duration_engine"]
    core_estimation_estimator["core.estimation.estimator"]
    core_formulas["core.formulas"]
    core_formulas_formulas["core.formulas.formulas"]
    core_risk["core.risk"]
    core_risk_risk_engine["core.risk.risk_engine"]
    core_scenario["core.scenario"]
    core_scenario_scenario_engine["core.scenario.scenario_engine"]
    main["main"]
    models["models"]
    models_app_settings["models.app_settings"]
    models_deliverables["models.deliverables"]
    models_estimation_result["models.estimation_result"]
    models_project["models.project"]
    models_project_parameters["models.project_parameters"]
    models_review_metrics["models.review_metrics"]
    models_scenario["models.scenario"]
    models_user_profile["models.user_profile"]
    persistence["persistence"]
    persistence_database["persistence.database"]
    persistence_estimation_repository["persistence.estimation_repository"]
    persistence_profile_repository["persistence.profile_repository"]
    persistence_project_repository["persistence.project_repository"]
    persistence_scenario_repository["persistence.scenario_repository"]
    persistence_settings_repository["persistence.settings_repository"]
    reports["reports"]
    reports_excel_report["reports.excel_report"]
    reports_pdf_report["reports.pdf_report"]
    reports_report_generator["reports.report_generator"]
    services["services"]
    services_estimation_service["services.estimation_service"]
    services_excel_export_service["services.excel_export_service"]
    services_pdf_export_service["services.pdf_export_service"]
    services_profile_service["services.profile_service"]
    services_project_service["services.project_service"]
    services_scenario_service["services.scenario_service"]
    services_settings_service["services.settings_service"]
    ui["ui"]
    ui_dashboard_tab["ui.dashboard_tab"]
    ui_estimation_tab["ui.estimation_tab"]
    ui_main_window["ui.main_window"]
    ui_profile_dialog["ui.profile_dialog"]
    ui_profiles_tab["ui.profiles_tab"]
    ui_project_dialog["ui.project_dialog"]
    ui_projects_tab["ui.projects_tab"]
    ui_reports_tab["ui.reports_tab"]
    ui_scenario_dialog["ui.scenario_dialog"]
    ui_scenarios_tab["ui.scenarios_tab"]
    ui_settings_dialog["ui.settings_dialog"]
    utils_exceptions["utils.exceptions"]
    utils_string_utils["utils.string_utils"]

```

## Diagramme des classes

```mermaid
classDiagram
    class EnsureDirectories {
    }
    class CostBreakdown {
        +float estimated_hours
        +float estimated_days
        +float daily_rate
        +float base_cost
        +float risk_factor
        +float final_cost
    }
    class CostEngine {
        +Any HOURS_PER_DAY
        +calculate(cls, estimated_hours, daily_rate, risk_factor, hours_per_day) CostBreakdown
        +from_days(cls, estimated_days, daily_rate, risk_factor, hours_per_day) CostBreakdown
        +margin(selling_price, estimated_cost) float
        +margin_rate(selling_price, estimated_cost) float
    }
    class DurationBreakdown {
        +float estimated_hours
        +float productivity_factor
        +float risk_factor
        +float availability_factor
        +float adjusted_hours
        +float estimated_days
    }
    class DurationEngine {
        +Any HOURS_PER_DAY
        +calculate(cls, estimated_hours, productivity_factor, risk_factor, availability_factor) DurationBreakdown
        +hours_to_days(cls, hours) float
        +days_to_hours(cls, days) float
        +working_weeks(estimated_days) float
    }
    class Estimator {
        +Any cost_engine
        +Any duration_engine
        +Any risk_engine
        +__init__() None
        +estimate(project, profile) EstimationResult
        +_calculate_hours(project) float
    }
    class RiskResult {
        +float score
        +float factor
    }
    class RiskEngine {
        +calculate(planning_risk, scope_risk, technical_risk) RiskResult
    }
    class ScenarioType {
        +Any OPTIMISTIC
        +Any REALISTIC
        +Any PESSIMISTIC
    }
    class ScenarioResult {
        +str scenario
        +float estimated_hours
        +float estimated_days
        +float estimated_cost
        +float effort_multiplier
        +float risk_multiplier
    }
    class ScenarioEngine {
        +Any SCENARIOS
        +build(cls, base_hours, base_days, base_cost, scenario_type) ScenarioResult
        +generate_all(cls, base_hours, base_days, base_cost) list[ScenarioResult]
        +best_case(scenarios) ScenarioResult
        +worst_case(scenarios) ScenarioResult
        +average_cost(scenarios) float
    }
    class AppSettings {
        +str company_name
        +str currency
        +str export_directory
        +float hours_per_day
        +int days_per_month
        +str theme
        +int font_size
        +bool show_dashboard_kpis
        +bool show_dashboard_charts
        +to_dict() dict
        +from_dict(cls, data) 'AppSettings'
    }
    class Deliverables {
        +int rapport_calcul
        +int rapport_calcul_intermediare
        +int fichier_resultat
        +int notes_supports
        +int notes_equipements
        +int plans_supports
        +int presentation_client
        +int fichier_modele
    }
    class EstimationResult {
        +int | None id
        +str estimation_nom
        +str project_nom
        +str profile_nom
        +str scenario_nom
        +float estimated_hours
        +float estimated_days
        +float estimated_cost
        +float risk_factor
        +str created_at
        +create(cls, project_nom, profile_nom, scenario_nom, estimated_hours, estimated_days, estimated_cost, risk_factor) None
    }
    class Project {
        +int | None id
        +str nom
        +str client
        +str description
        +str profile_nom
        +float budget
        +str status
        +ProjectParameters parameters
        +Deliverables deliverables
        +ReviewMetrics reviews
    }
    class ProjectParameters {
        +int nb_lignes
        +int nb_supports
        +int nb_vannes
        +int nb_brides
        +int nb_compensateur
        +int nb_connexions_equipements
        +int nb_soudures
    }
    class ReviewMetrics {
        +int nb_revues_internes
        +int nb_revues_client
        +int nb_aller_retour
    }
    class Scenario {
        +int | None id
        +str nom
        +str description
        +float facteur_productivite
        +float facteur_risque
        +float facteur_disponibilite
        +bool actif
    }
    class UserProfile {
        +int | None id
        +str nom
        +str description
        +float taux_journalier
        +float heures_par_jour
        +float facteur_productivite
        +float heure_par_ligne
        +float heure_par_support
        +float heure_par_vanne
        +float heure_par_boite_a_ressort
        +float heure_compensateur
        +float heure_par_bride
        +float heure_par_equipement
        +float heure_par_note_de_calcul
        +float heure_par_presentation
        +float heure_par_verification
    }
    class Database {
        +initialize() None
    }
    class EstimationRepository {
        +save(estimation) None
        +get_all() list[EstimationResult]
        +get_estimation(estimation_id) EstimationResult | None
        +delete_estimation(estimation_id) None
        +rename_estimation(estimation_id, new_name) None
        +duplicate_estimation(estimation_id) int | None
        +count() int
    }
    class ProfileRepository {
        +create(profile) int
        +get_by_id(profile_id) UserProfile | None
        +get_all() list[UserProfile]
        +update(profile) bool
        +delete(profile_id) bool
        +count() int
        +get_by_name(nom) UserProfile | None
    }
    class ProjectRepository {
        +Any storage_dir
        +__init__(storage_dir) None
        +_name_exists(project_nom) bool
        +save(project) Project
        +delete(project_nom) bool
        +load(project_nom) Project
        +get_by_name(nom) Project | None
        +get_by_id(project_id) Project | None
        +get_all() list[Project]
        +exists(project_nom) bool
        +list_projects() list[str]
        +update(project) Project
        +count() int
    }
    class ScenarioRepository {
        +_name_exists(nom, exclude_id) bool
        +create(scenario) int
        +get_by_id(scenario_id) Scenario | None
        +get_by_name(nom) Scenario | None
        +get_all() list[Scenario]
        +update(scenario) bool
        +is_used(scenario_id) bool
        +delete(scenario_id) bool
        +count() int
    }
    class SettingsRepository {
        +Any data_dir
        +Any file_path
        +__init__(data_dir) None
        +load() AppSettings
        +save(settings) None
        +reset() AppSettings
    }
    class ExcelReport {
        +generate(estimation, output_file) None
    }
    class PdfReport {
        +generate(estimation, output_file) None
    }
    class ReportGenerator {
        +generate(report_type, estimation, output_file) None
    }
    class EstimationService {
        +Any repository
        +Any estimator
        +__init__(repository) None
        +estimate(project, profile, scenario) EstimationResult
    }
    class ExcelExportService {
        +export(report, file_path, currency) Path
        +_get_versioned_filename(output) Path
    }
    class PdfExportService {
        +export(report, file_path, currency) Path
        +_get_versioned_filename(output) Path
    }
    class ProfileService {
        +Any repository
        +__init__(repository) None
        +create_profile(profile) int
        +update_profile(profile) bool
        +delete_profile(profile_id) bool
        +get_profile(profile_id) UserProfile | None
        +get_profile_by_nom(nom) UserProfile | None
        +get_all_profiles() list[UserProfile]
        +get_default_profile() UserProfile | None
        +set_default_profile() bool
        +validate_profile(profile) tuple[bool, list[str]]
        +duplicate_profile(profile_id, new_nom) int
        +count_profiles() int
    }
    class ProjectService {
        +Any repository
        +__init__(repository) None
        +create_project(project) Project
        +update_project(project) Project
        +delete_project(project_nom) bool
        +get_project(project_nom) Project | None
        +get_project_by_nom(nom) Project | None
        +get_all_projects() list[Project]
        +search_projects(keyword) list[Project]
        +count_projects() int
        +total_estimated_cost() float
        +total_estimated_days() float
        +total_estimated_hours() float
        +build_estimation_context(project_nom) dict
        +_validate_project(project) None
        +dashboard_summary() dict
    }
    class ScenarioService {
        +Any repository
        +__init__() None
        +get_all_scenarios() list[Scenario]
        +get_scenario(scenario_id) Scenario | None
        +get_by_name(nom) Scenario | None
        +create_scenario(scenario) int
        +update_scenario(scenario) None
        +delete_scenario(scenario_id) None
        +count() int
        +_validate_scenario(scenario) None
    }
    class SettingsService {
        +Any persistence
        +__init__(repository) None
        +get() AppSettings
        +save(settings) None
        +reset() AppSettings
        +update(**kwargs) AppSettings
        +_validate(settings) None
    }
    class DashboardTab {
        +Any estimation_repository
        +Any settings_service
        +Any settings
        +Any lbl_count
        +Any lbl_hours
        +Any lbl_days
        +Any lbl_cost
        +Any lbl_total_cost
        +Any lbl_max_cost
        +Any lbl_min_cost
        +Any lbl_best_profile
        +Any lbl_last_estimation
        +Any figure
        +Any canvas
        +Any cost_figure
        +Any cost_canvas
        +Any top_table
        +Any table
        +__init__(estimation_repository, settings_service, parent) None
        +_build_ui() None
        +load_data() None
        +_update_chart(reports) None
        +_update_cost_chart(reports) None
        +refresh() None
    }
    class EstimationTab {
        +Any settings_service
        +Any settings
        +Any estimation_service
        +Any profile_service
        +Any project_service
        +Any scenario_service
        +Any profile_combo
        +Any project_combo
        +Any scenario_combo
        +Any estimate_button
        +Any hours_edit
        +Any days_edit
        +Any cost_edit
        +Any cost_label
        +Any details_text
        +__init__(settings_service, parent) None
        +_build_ui() None
        +_load_data() None
        +calculate_estimation() None
        +_display_details(project, profile, scenario, result) None
        +_update_labels() None
        +refresh() None
    }
    class MainWindow {
        +Any settings_service
        +Any settings
        +Any estimation_repository
        +Any tabs
        +Any projects_tab
        +Any profiles_tab
        +Any estimation_tab
        +Any scenarios_tab
        +Any reports_tab
        +Any dashboard_tab
        +__init__(settings_service) None
        +_create_ui() None
        +_create_menu() None
        +_create_statusbar() None
        +run_estimation() None
        +show_about() None
        +on_tab_changed(index) None
        +show_settings() None
        +reload_settings() None
        +closeEvent(event) None
    }
    class ProfileDialog {
        +Any profile
        +Any nom_edit
        +Any description_edit
        +Any taux_journalier_edit
        +Any heures_par_jour_edit
        +Any facteur_productivite_edit
        +Any heure_par_ligne_edit
        +Any heure_par_support_edit
        +Any heure_par_vanne_edit
        +Any heure_par_boite_a_ressort_edit
        +Any heure_compensateur_edit
        +Any heure_par_bride_edit
        +Any heure_par_equipement_edit
        +__init__(parent, profile) None
        +_build_ui() None
        +_create_time_spin() None
        +_load_profile() None
        +get_profile() UserProfile
    }
    class ProfilesTab {
        +Any settings_service
        +Any settings
        +Any profile_service
        +Any profile_table
        +Any details_label
        +Any btn_add
        +Any btn_edit
        +Any btn_delete
        +Any btn_refresh
        +__init__(settings_service, parent) None
        +_build_ui() None
        +load_profiles() None
        +on_profile_selected() None
        +add_profile() None
        +edit_profile() None
        +delete_profile() None
        +get_selected_profile() None
        +_update_labels() None
        +refresh() None
    }
    class ProjectDialog {
        +Any project
        +Any nom_edit
        +Any client_edit
        +Any description_edit
        +Any nb_lignes_edit
        +Any nb_supports_edit
        +Any nb_vannes_edit
        +Any nb_brides_edit
        +Any nb_compensateur_edit
        +Any nb_connexions_edit
        +Any nb_soudures_edit
        +Any rapport_calcul_edit
        +Any rapport_inter_edit
        +Any notes_supports_edit
        +Any notes_equipements_edit
        +Any plans_supports_edit
        +Any presentation_client_edit
        +Any fichier_modele_edit
        +Any fichier_resultat_edit
        +Any revues_internes_edit
        +Any revues_client_edit
        +Any aller_retour_edit
        +__init__(project, parent) None
        +_build_ui() None
        +_load_project() None
        +get_project() None
    }
    class ProjectsTab {
        +Any project_service
        +Any btn_new
        +Any btn_edit
        +Any btn_delete
        +Any btn_refresh
        +Any table
        +Any details_label
        +__init__(parent) None
        +_build_ui() None
        +load_projects() None
        +get_selected_project() None
        +create_project() None
        +edit_project() None
        +delete_project() None
        +on_project_selected() None
        +refresh() None
    }
    class NumericTableWidgetItem {
        +__lt__(other) None
    }
    class ReportsTab {
        +Any estimation_repository
        +Any settings_service
        +Any settings
        +Any pdf_export_service
        +Any excel_export_service
        +Any reports_table
        +Any open_btn
        +Any rename_btn
        +Any delete_btn
        +Any refresh_btn
        +Any open_exports_btn
        +Any pdf_btn
        +Any excel_btn
        +Any lbl_name
        +Any lbl_project
        +Any lbl_scenario
        +Any lbl_budget
        +Any lbl_date
        +__init__(estimation_repository, settings_service, parent) None
        +_build_ui() None
        +load_reports() None
        +_get_selected_report() None
        +_update_details() None
        +_open_report() None
        +rename_report() None
        +delete_report() None
        +export_pdf() None
        +export_excel() None
        +open_exports_folder() None
    }
    class ScenarioDialog {
        +Any scenario
        +Any nom_edit
        +Any description_edit
        +Any productivite_edit
        +Any risque_edit
        +Any disponibilite_edit
        +Any actif_check
        +__init__(parent, scenario) None
        +_build_ui() None
        +_load_scenario() None
        +get_scenario() Scenario
    }
    class ScenariosTab {
        +Any service
        +Any add_button
        +Any edit_button
        +Any delete_button
        +Any refresh_button
        +Any table
        +Any details_text
        +Any scenarios
        +__init__(parent) None
        +_build_ui() None
        +load_scenarios() None
        +get_selected_scenario() None
        +add_scenario() None
        +edit_scenario() None
        +delete_scenario() None
        +_show_details() None
        +refresh() None
    }
    class SettingsDialog {
        +Any settings_service
        +Any settings
        +Any tabs
        +Any company_edit
        +Any currency_combo
        +Any export_directory_edit
        +Any hours_per_day_spin
        +Any days_per_month_spin
        +Any theme_combo
        +Any font_size_spin
        +Any dashboard_kpis_check
        +Any dashboard_charts_check
        +Any buttons
        +__init__(settings_service, parent) None
        +_create_ui() None
        +_load_settings() None
        +_save() None
    }
    class EstimateFlexError {
    }
    class ValidationError {
    }
    class DatabaseError {
    }
    class EstimationError {
    }
    class ReportGenerationError {
    }

    EstimateFlexError <|-- DatabaseError
    EstimateFlexError <|-- EstimationError
    EstimateFlexError <|-- ReportGenerationError
    EstimateFlexError <|-- ValidationError
    CostEngine ..> CostBreakdown
    DashboardTab ..> SettingsService
    DurationEngine ..> DurationBreakdown
    EstimationRepository ..> EstimationResult
    EstimationService ..> EstimationRepository
    EstimationService ..> EstimationResult
    EstimationService ..> Estimator
    EstimationService ..> Project
    EstimationService ..> Scenario
    EstimationService ..> UserProfile
    EstimationTab ..> EstimationService
    EstimationTab ..> ProfileService
    EstimationTab ..> ProjectService
    EstimationTab ..> ScenarioService
    Estimator ..> CostEngine
    Estimator ..> DurationEngine
    Estimator ..> EstimationResult
    Estimator ..> Project
    Estimator ..> RiskEngine
    Estimator ..> UserProfile
    MainWindow ..> DashboardTab
    MainWindow ..> EstimationRepository
    MainWindow ..> EstimationTab
    MainWindow ..> ProfilesTab
    MainWindow ..> ProjectsTab
    MainWindow ..> ReportsTab
    MainWindow ..> ScenariosTab
    MainWindow ..> SettingsDialog
    MainWindow ..> SettingsService
    ProfileDialog ..> UserProfile
    ProfileRepository ..> UserProfile
    ProfileService ..> ProfileRepository
    ProfileService ..> UserProfile
    ProfilesTab ..> ProfileDialog
    ProfilesTab ..> ProfileService
    ProjectDialog ..> Deliverables
    ProjectDialog ..> Project
    ProjectDialog ..> ProjectParameters
    ProjectDialog ..> ReviewMetrics
    ProjectRepository ..> Deliverables
    ProjectRepository ..> Project
    ProjectRepository ..> ProjectParameters
    ProjectRepository ..> ReviewMetrics
    ProjectService ..> Project
    ProjectService ..> ProjectRepository
    ProjectService ..> ValidationError
    ProjectsTab ..> ProjectDialog
    ProjectsTab ..> ProjectService
    ReportsTab ..> ExcelExportService
    ReportsTab ..> NumericTableWidgetItem
    ReportsTab ..> PdfExportService
    ReportsTab ..> SettingsService
    RiskEngine ..> RiskResult
    ScenarioDialog ..> Scenario
    ScenarioEngine ..> ScenarioResult
    ScenarioEngine ..> ScenarioType
    ScenarioRepository ..> Scenario
    ScenarioService ..> Scenario
    ScenarioService ..> ScenarioRepository
    ScenariosTab ..> ScenarioDialog
    ScenariosTab ..> ScenarioService
    SettingsDialog ..> AppSettings
    SettingsDialog ..> SettingsService
    SettingsRepository ..> AppSettings
    SettingsService ..> AppSettings
    SettingsService ..> SettingsRepository
```

## Dépendances circulaires

Aucune dépendance circulaire détectée.

## Modules

### ``

Fichier : `src\__init__.py`

### `config`

Fichier : `src\config\__init__.py`

### `config.paths`

Fichier : `src\config\paths.py`

#### Classes

##### `EnsureDirectories`

### `core`

Fichier : `src\core\__init__.py`

### `core.constants`

Fichier : `src\core\constants.py`

### `core.estimation`

Fichier : `src\core\estimation\__init__.py`

### `core.estimation.cost_engine`

Fichier : `src\core\estimation\cost_engine.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `CostBreakdown` — dataclass

**Attributs de classe :**

- `estimated_hours`: `float`
- `estimated_days`: `float`
- `daily_rate`: `float`
- `base_cost`: `float`
- `risk_factor`: `float`
- `final_cost`: `float`

##### `CostEngine`

**Attributs de classe :**

- `HOURS_PER_DAY`

**Méthodes :**

- `calculate(cls, estimated_hours: float, daily_rate: float, risk_factor: float, hours_per_day: float | None) -> CostBreakdown`
- `from_days(cls, estimated_days: float, daily_rate: float, risk_factor: float, hours_per_day: float | None) -> CostBreakdown`
- `margin(selling_price: float, estimated_cost: float) -> float`
- `margin_rate(selling_price: float, estimated_cost: float) -> float`

### `core.estimation.duration_engine`

Fichier : `src\core\estimation\duration_engine.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `DurationBreakdown` — dataclass

**Attributs de classe :**

- `estimated_hours`: `float`
- `productivity_factor`: `float`
- `risk_factor`: `float`
- `availability_factor`: `float`
- `adjusted_hours`: `float`
- `estimated_days`: `float`

##### `DurationEngine`

**Attributs de classe :**

- `HOURS_PER_DAY`

**Méthodes :**

- `calculate(cls, estimated_hours: float, productivity_factor: float, risk_factor: float, availability_factor: float) -> DurationBreakdown`
- `hours_to_days(cls, hours: float) -> float`
- `days_to_hours(cls, days: float) -> float`
- `working_weeks(estimated_days: float) -> float`

### `core.estimation.estimator`

Fichier : `src\core\estimation\estimator.py`

**From imports :**

- `src.core.estimation.cost_engine:CostEngine`
- `src.core.estimation.duration_engine:DurationEngine`
- `src.core.risk.risk_engine:RiskEngine`
- `src.models.estimation_result:EstimationResult`
- `src.models.project:Project`
- `src.models.user_profile:UserProfile`

#### Classes

##### `Estimator`

**Attributs d'instance :**

- `cost_engine` (valeur `CostEngine()`)
- `duration_engine` (valeur `DurationEngine()`)
- `risk_engine` (valeur `RiskEngine()`)

**Méthodes :**

- `__init__(self) -> None`
- `estimate(self, project: Project, profile: UserProfile) -> EstimationResult`
- `_calculate_hours(self, project: Project) -> float`

### `core.formulas`

Fichier : `src\core\formulas\__init__.py`

### `core.formulas.formulas`

Fichier : `src\core\formulas\formulas.py`

**From imports :**

- `src.models.deliverables:Deliverables`
- `src.models.project_parameters:ProjectParameters`
- `src.models.review_metrics:ReviewMetrics`
- `src.models.user_profile:UserProfile`

#### Fonctions top-level

- `effort_lignes(nb_lignes: int, heure_par_ligne: float) -> float`
- `effort_supports(nb_supports: int, heure_par_support: float) -> float`
- `effort_vannes(nb_vannes: int, heure_par_vanne: float) -> float`
- `effort_brides(nb_brides: int, heure_par_bride: float) -> float`
- `effort_equipements(nb_connexions: int, heure_par_equipement: float) -> float`
- `effort_rapport_calcul(nb_rapports: int, heure_par_note: float) -> float`
- `effort_notes_supports(nb_notes: int, heure_par_note: float) -> float`
- `effort_notes_equipements(nb_notes: int, heure_par_note: float) -> float`
- `effort_plans_supports(nb_plans: int, heure_par_note: float) -> float`
- `effort_presentation_client(nb_presentations: int, heure_par_presentation: float) -> float`
- `effort_revue_interne(nb_revues: int, heure_par_verification: float) -> float`
- `effort_revue_client(nb_revues: int, heure_par_verification: float) -> float`
- `effort_aller_retour(nb_allers_retours: int, heure_par_verification: float) -> float`
- `calcul_effort_modelisation(project: ProjectParameters, profile: UserProfile) -> float`
- `calcul_effort_redaction(deliverables: Deliverables, profile: UserProfile) -> float`
- `calcul_effort_verification(reviews: ReviewMetrics, profile: UserProfile) -> float`
- `calcul_effort_total(effort_modelisation: float, effort_redaction: float, effort_verification: float) -> float`
- `calcul_taux_horaire(profile: UserProfile) -> float`
- `calcul_cout(effort_h: float, profile: UserProfile) -> float`
- `calcul_cout_total(cout_modelisation: float, cout_redaction: float, cout_verification: float) -> float`
- `calcul_estimation(project: ProjectParameters, deliverables: Deliverables, reviews: ReviewMetrics, profile: UserProfile) -> dict`

### `core.risk`

Fichier : `src\core\risk\__init__.py`

### `core.risk.risk_engine`

Fichier : `src\core\risk\risk_engine.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `RiskResult` — dataclass

**Attributs de classe :**

- `score`: `float`
- `factor`: `float`

##### `RiskEngine`

**Méthodes :**

- `calculate(planning_risk: int, scope_risk: int, technical_risk: int) -> RiskResult`

### `core.scenario`

Fichier : `src\core\scenario\__init__.py`

### `core.scenario.scenario_engine`

Fichier : `src\core\scenario\scenario_engine.py`

**From imports :**

- `dataclasses:dataclass`
- `enum:StrEnum`

#### Classes

##### `ScenarioType` — Enum

**Héritage :** `StrEnum`

**Attributs de classe :**

- `OPTIMISTIC`
- `REALISTIC`
- `PESSIMISTIC`

##### `ScenarioResult` — dataclass

**Attributs de classe :**

- `scenario`: `str`
- `estimated_hours`: `float`
- `estimated_days`: `float`
- `estimated_cost`: `float`
- `effort_multiplier`: `float`
- `risk_multiplier`: `float`

##### `ScenarioEngine`

**Attributs de classe :**

- `SCENARIOS`

**Méthodes :**

- `build(cls, base_hours: float, base_days: float, base_cost: float, scenario_type: ScenarioType) -> ScenarioResult`
- `generate_all(cls, base_hours: float, base_days: float, base_cost: float) -> list[ScenarioResult]`
- `best_case(scenarios: list[ScenarioResult]) -> ScenarioResult`
- `worst_case(scenarios: list[ScenarioResult]) -> ScenarioResult`
- `average_cost(scenarios: list[ScenarioResult]) -> float`

### `main`

Fichier : `src\main.py`

**Imports :**

- `logging`
- `sys`
- `traceback`

**From imports :**

- `PyQt6.QtWidgets:QApplication`
- `PyQt6.QtWidgets:QMessageBox`
- `__future__:annotations`
- `src.config.paths:EnsureDirectories`
- `src.persistence.database:Database`
- `src.persistence.settings_repository:SettingsRepository`
- `src.services.settings_service:SettingsService`
- `src.ui.main_window:MainWindow`

#### Fonctions top-level

- `configure_logging() -> None`
- `initialize_application() -> None`
- `handle_exception(exc_type, exc_value, exc_traceback) -> None`
- `main() -> int`

### `models`

Fichier : `src\models\__init__.py`

### `models.app_settings`

Fichier : `src\models\app_settings.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `AppSettings` — dataclass

**Attributs de classe :**

- `company_name`: `str`
- `currency`: `str`
- `export_directory`: `str`
- `hours_per_day`: `float`
- `days_per_month`: `int`
- `theme`: `str`
- `font_size`: `int`
- `show_dashboard_kpis`: `bool`
- `show_dashboard_charts`: `bool`

**Méthodes :**

- `to_dict(self) -> dict`
- `from_dict(cls, data: dict) -> 'AppSettings'`

### `models.deliverables`

Fichier : `src\models\deliverables.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `Deliverables` — dataclass

**Attributs de classe :**

- `rapport_calcul`: `int`
- `rapport_calcul_intermediare`: `int`
- `fichier_resultat`: `int`
- `notes_supports`: `int`
- `notes_equipements`: `int`
- `plans_supports`: `int`
- `presentation_client`: `int`
- `fichier_modele`: `int`

### `models.estimation_result`

Fichier : `src\models\estimation_result.py`

**From imports :**

- `dataclasses:dataclass`
- `datetime:datetime`

#### Classes

##### `EstimationResult` — dataclass

**Attributs de classe :**

- `id`: `int | None`
- `estimation_nom`: `str`
- `project_nom`: `str`
- `profile_nom`: `str`
- `scenario_nom`: `str`
- `estimated_hours`: `float`
- `estimated_days`: `float`
- `estimated_cost`: `float`
- `risk_factor`: `float`
- `created_at`: `str`

**Méthodes :**

- `create(cls, project_nom: str, profile_nom: str, scenario_nom: str, estimated_hours: float, estimated_days: float, estimated_cost: float, risk_factor: float) -> None`

### `models.project`

Fichier : `src\models\project.py`

**From imports :**

- `.deliverables:Deliverables`
- `.project_parameters:ProjectParameters`
- `.review_metrics:ReviewMetrics`
- `dataclasses:dataclass`
- `dataclasses:field`

#### Classes

##### `Project` — dataclass

**Attributs de classe :**

- `id`: `int | None`
- `nom`: `str`
- `client`: `str`
- `description`: `str`
- `profile_nom`: `str`
- `budget`: `float`
- `status`: `str`
- `parameters`: `ProjectParameters`
- `deliverables`: `Deliverables`
- `reviews`: `ReviewMetrics`

### `models.project_parameters`

Fichier : `src\models\project_parameters.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `ProjectParameters` — dataclass

**Attributs de classe :**

- `nb_lignes`: `int`
- `nb_supports`: `int`
- `nb_vannes`: `int`
- `nb_brides`: `int`
- `nb_compensateur`: `int`
- `nb_connexions_equipements`: `int`
- `nb_soudures`: `int`

### `models.review_metrics`

Fichier : `src\models\review_metrics.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `ReviewMetrics` — dataclass

**Attributs de classe :**

- `nb_revues_internes`: `int`
- `nb_revues_client`: `int`
- `nb_aller_retour`: `int`

### `models.scenario`

Fichier : `src\models\scenario.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `Scenario` — dataclass

**Attributs de classe :**

- `id`: `int | None`
- `nom`: `str`
- `description`: `str`
- `facteur_productivite`: `float`
- `facteur_risque`: `float`
- `facteur_disponibilite`: `float`
- `actif`: `bool`

### `models.user_profile`

Fichier : `src\models\user_profile.py`

**From imports :**

- `dataclasses:dataclass`

#### Classes

##### `UserProfile` — dataclass

**Attributs de classe :**

- `id`: `int | None`
- `nom`: `str`
- `description`: `str`
- `taux_journalier`: `float`
- `heures_par_jour`: `float`
- `facteur_productivite`: `float`
- `heure_par_ligne`: `float`
- `heure_par_support`: `float`
- `heure_par_vanne`: `float`
- `heure_par_boite_a_ressort`: `float`
- `heure_compensateur`: `float`
- `heure_par_bride`: `float`
- `heure_par_equipement`: `float`
- `heure_par_note_de_calcul`: `float`
- `heure_par_presentation`: `float`
- `heure_par_verification`: `float`

### `persistence`

Fichier : `src\persistence\__init__.py`

### `persistence.database`

Fichier : `src\persistence\database.py`

**Imports :**

- `sqlite3`
- `sys`

**From imports :**

- `pathlib:Path`

#### Classes

##### `Database`

**Méthodes :**

- `initialize(self) -> None`

#### Fonctions top-level

- `get_database_path() -> Path`
- `get_connection() -> None`
- `test_connection() -> bool`

### `persistence.estimation_repository`

Fichier : `src\persistence\estimation_repository.py`

**From imports :**

- `datetime:datetime`
- `src.models.estimation_result:EstimationResult`
- `src.persistence.database:get_connection`

#### Classes

##### `EstimationRepository`

**Méthodes :**

- `save(self, estimation: EstimationResult) -> None`
- `get_all(self) -> list[EstimationResult]`
- `get_estimation(self, estimation_id: int) -> EstimationResult | None`
- `delete_estimation(self, estimation_id: int) -> None`
- `rename_estimation(self, estimation_id: int, new_name: str) -> None`
- `duplicate_estimation(self, estimation_id: int) -> int | None`
- `count(self) -> int`

### `persistence.profile_repository`

Fichier : `src\persistence\profile_repository.py`

**From imports :**

- `src.models.user_profile:UserProfile`
- `src.persistence.database:get_connection`

#### Classes

##### `ProfileRepository`

**Méthodes :**

- `create(profile: UserProfile) -> int`
- `get_by_id(profile_id: int) -> UserProfile | None`
- `get_all() -> list[UserProfile]`
- `update(profile: UserProfile) -> bool`
- `delete(profile_id: int) -> bool`
- `count() -> int`
- `get_by_name(nom: str) -> UserProfile | None`

### `persistence.project_repository`

Fichier : `src\persistence\project_repository.py`

**Imports :**

- `json`

**From imports :**

- `__future__:annotations`
- `dataclasses:asdict`
- `pathlib:Path`
- `src.models.deliverables:Deliverables`
- `src.models.project:Project`
- `src.models.project_parameters:ProjectParameters`
- `src.models.review_metrics:ReviewMetrics`
- `src.utils.string_utils:normalize_name`

#### Classes

##### `ProjectRepository`

**Attributs d'instance :**

- `storage_dir` (valeur `Path(storage_dir)`)

**Méthodes :**

- `__init__(self, storage_dir: str | Path) -> None`
- `_name_exists(self, project_nom: str) -> bool`
- `save(self, project: Project) -> Project`
- `delete(self, project_nom: str) -> bool`
- `load(self, project_nom: str) -> Project`
- `get_by_name(self, nom: str) -> Project | None`
- `get_by_id(self, project_id: int) -> Project | None`
- `get_all(self) -> list[Project]`
- `exists(self, project_nom: str) -> bool`
- `list_projects(self) -> list[str]`
- `update(self, project: Project) -> Project`
- `count(self) -> int`

### `persistence.scenario_repository`

Fichier : `src\persistence\scenario_repository.py`

**From imports :**

- `src.models.scenario:Scenario`
- `src.persistence.database:get_connection`
- `src.utils.string_utils:normalize_name`

#### Classes

##### `ScenarioRepository`

**Méthodes :**

- `_name_exists(nom: str, exclude_id: int | None) -> bool`
- `create(scenario: Scenario) -> int`
- `get_by_id(scenario_id: int) -> Scenario | None`
- `get_by_name(nom: str) -> Scenario | None`
- `get_all() -> list[Scenario]`
- `update(scenario: Scenario) -> bool`
- `is_used(scenario_id: int) -> bool`
- `delete(scenario_id: int) -> bool`
- `count() -> int`

### `persistence.settings_repository`

Fichier : `src\persistence\settings_repository.py`

**Imports :**

- `json`

**From imports :**

- `__future__:annotations`
- `pathlib:Path`
- `src.models.app_settings:AppSettings`

#### Classes

##### `SettingsRepository`

**Attributs d'instance :**

- `data_dir` (valeur `Path(data_dir)`)
- `file_path` (valeur `self.data_dir / 'settings.json'`)

**Méthodes :**

- `__init__(self, data_dir: str | Path) -> None`
- `load(self) -> AppSettings`
- `save(self, settings: AppSettings) -> None`
- `reset(self) -> AppSettings`

### `reports`

Fichier : `src\reports\__init__.py`

### `reports.excel_report`

Fichier : `src\reports\excel_report.py`

**From imports :**

- `openpyxl:Workbook`

#### Classes

##### `ExcelReport`

**Méthodes :**

- `generate(estimation, output_file) -> None`

### `reports.pdf_report`

Fichier : `src\reports\pdf_report.py`

**From imports :**

- `reportlab.lib.styles:getSampleStyleSheet`
- `reportlab.platypus:Paragraph`
- `reportlab.platypus:SimpleDocTemplate`
- `reportlab.platypus:Spacer`

#### Classes

##### `PdfReport`

**Méthodes :**

- `generate(estimation, output_file) -> None`

### `reports.report_generator`

Fichier : `src\reports\report_generator.py`

**From imports :**

- `src.reports.excel_report:ExcelReport`
- `src.reports.pdf_report:PdfReport`

#### Classes

##### `ReportGenerator`

**Méthodes :**

- `generate(report_type, estimation, output_file) -> None`

### `services`

Fichier : `src\services\__init__.py`

### `services.estimation_service`

Fichier : `src\services\estimation_service.py`

**From imports :**

- `datetime:datetime`
- `src.core.estimation.estimator:Estimator`
- `src.models.estimation_result:EstimationResult`
- `src.models.project:Project`
- `src.models.scenario:Scenario`
- `src.models.user_profile:UserProfile`
- `src.persistence.estimation_repository:EstimationRepository`

#### Classes

##### `EstimationService`

**Attributs d'instance :**

- `repository` (valeur `repository or EstimationRepository()`)
- `estimator` (valeur `Estimator()`)

**Méthodes :**

- `__init__(self, repository: EstimationRepository | None) -> None`
- `estimate(self, project: Project, profile: UserProfile, scenario: Scenario) -> EstimationResult`

### `services.excel_export_service`

Fichier : `src\services\excel_export_service.py`

**From imports :**

- `openpyxl.styles:Alignment`
- `openpyxl.styles:Border`
- `openpyxl.styles:Font`
- `openpyxl.styles:PatternFill`
- `openpyxl.styles:Side`
- `openpyxl:Workbook`
- `pathlib:Path`

#### Classes

##### `ExcelExportService`

**Méthodes :**

- `export(report, file_path: str, currency: str) -> Path`
- `_get_versioned_filename(output: Path) -> Path`

### `services.pdf_export_service`

Fichier : `src\services\pdf_export_service.py`

**From imports :**

- `pathlib:Path`
- `reportlab.lib.enums:TA_LEFT`
- `reportlab.lib.styles:ParagraphStyle`
- `reportlab.lib.styles:getSampleStyleSheet`
- `reportlab.lib:colors`
- `reportlab.platypus:Image`
- `reportlab.platypus:Paragraph`
- `reportlab.platypus:SimpleDocTemplate`
- `reportlab.platypus:Spacer`
- `reportlab.platypus:Table`
- `reportlab.platypus:TableStyle`

#### Classes

##### `PdfExportService`

**Méthodes :**

- `export(report, file_path: str, currency: str) -> Path`
- `_get_versioned_filename(output: Path) -> Path`

### `services.profile_service`

Fichier : `src\services\profile_service.py`

**From imports :**

- `__future__:annotations`
- `dataclasses:replace`
- `src.models.user_profile:UserProfile`
- `src.persistence.profile_repository:ProfileRepository`

#### Classes

##### `ProfileService`

**Attributs d'instance :**

- `repository` (valeur `repository or ProfileRepository()`)

**Méthodes :**

- `__init__(self, repository: ProfileRepository | None) -> None`
- `create_profile(self, profile: UserProfile) -> int`
- `update_profile(self, profile: UserProfile) -> bool`
- `delete_profile(self, profile_id: int) -> bool`
- `get_profile(self, profile_id: int) -> UserProfile | None`
- `get_profile_by_nom(self, nom: str) -> UserProfile | None`
- `get_all_profiles(self) -> list[UserProfile]`
- `get_default_profile(self) -> UserProfile | None`
- `set_default_profile(self) -> bool`
- `validate_profile(self, profile: UserProfile) -> tuple[bool, list[str]]`
- `duplicate_profile(self, profile_id: int, new_nom: str) -> int`
- `count_profiles(self) -> int`

### `services.project_service`

Fichier : `src\services\project_service.py`

**From imports :**

- `__future__:annotations`
- `src.models.project:Project`
- `src.persistence.project_repository:ProjectRepository`
- `src.utils.exceptions:ValidationError`
- `src.utils.string_utils:normalize_name`

#### Classes

##### `ProjectService`

**Attributs d'instance :**

- `repository` (valeur `repository or ProjectRepository()`)

**Méthodes :**

- `__init__(self, repository: ProjectRepository | None) -> None`
- `create_project(self, project: Project) -> Project`
- `update_project(self, project: Project) -> Project`
- `delete_project(self, project_nom: str) -> bool`
- `get_project(self, project_nom: str) -> Project | None`
- `get_project_by_nom(self, nom: str) -> Project | None`
- `get_all_projects(self) -> list[Project]`
- `search_projects(self, keyword: str) -> list[Project]`
- `count_projects(self) -> int`
- `total_estimated_cost(self) -> float`
- `total_estimated_days(self) -> float`
- `total_estimated_hours(self) -> float`
- `build_estimation_context(self, project_nom: str) -> dict`
- `_validate_project(self, project: Project) -> None`
- `dashboard_summary(self) -> dict`

### `services.scenario_service`

Fichier : `src\services\scenario_service.py`

**From imports :**

- `src.models.scenario:Scenario`
- `src.persistence.scenario_repository:ScenarioRepository`

#### Classes

##### `ScenarioService`

**Attributs d'instance :**

- `repository` (valeur `ScenarioRepository()`)

**Méthodes :**

- `__init__(self) -> None`
- `get_all_scenarios(self) -> list[Scenario]`
- `get_scenario(self, scenario_id: int) -> Scenario | None`
- `get_by_name(self, nom: str) -> Scenario | None`
- `create_scenario(self, scenario: Scenario) -> int`
- `update_scenario(self, scenario: Scenario) -> None`
- `delete_scenario(self, scenario_id: int) -> None`
- `count(self) -> int`
- `_validate_scenario(self, scenario: Scenario) -> None`

### `services.settings_service`

Fichier : `src\services\settings_service.py`

**From imports :**

- `__future__:annotations`
- `src.models.app_settings:AppSettings`
- `src.persistence.settings_repository:SettingsRepository`

#### Classes

##### `SettingsService`

**Attributs d'instance :**

- `persistence` (valeur `repository`)

**Méthodes :**

- `__init__(self, repository: SettingsRepository) -> None`
- `get(self) -> AppSettings`
- `save(self, settings: AppSettings) -> None`
- `reset(self) -> AppSettings`
- `update(self, **kwargs) -> AppSettings`
- `_validate(self, settings: AppSettings) -> None`

### `ui`

Fichier : `src\ui\__init__.py`

### `ui.dashboard_tab`

Fichier : `src\ui\dashboard_tab.py`

**From imports :**

- `PyQt6.QtCore:Qt`
- `PyQt6.QtWidgets:QAbstractItemView`
- `PyQt6.QtWidgets:QGridLayout`
- `PyQt6.QtWidgets:QGroupBox`
- `PyQt6.QtWidgets:QHBoxLayout`
- `PyQt6.QtWidgets:QLabel`
- `PyQt6.QtWidgets:QPushButton`
- `PyQt6.QtWidgets:QTableWidget`
- `PyQt6.QtWidgets:QTableWidgetItem`
- `PyQt6.QtWidgets:QVBoxLayout`
- `PyQt6.QtWidgets:QWidget`
- `collections:Counter`
- `matplotlib.backends.backend_qtagg:FigureCanvasQTAgg`
- `matplotlib.figure:Figure`
- `matplotlib.ticker:FuncFormatter`
- `src.services.settings_service:SettingsService`
- `statistics:mean`

#### Classes

##### `DashboardTab`

**Héritage :** `QWidget`

**Attributs d'instance :**

- `estimation_repository` (valeur `estimation_repository`)
- `settings_service` (valeur `settings_service`)
- `settings` (valeur `self.settings_service.get()`)
- `lbl_count` (valeur `QLabel('0')`)
- `lbl_hours` (valeur `QLabel('0 h')`)
- `lbl_days` (valeur `QLabel('0 j')`)
- `lbl_cost` (valeur `QLabel(f'0 {self.settings.currency}')`)
- `lbl_total_cost` (valeur `QLabel(f'0 {self.settings.currency}')`)
- `lbl_max_cost` (valeur `QLabel(f'0 {self.settings.currency}')`)
- `lbl_min_cost` (valeur `QLabel(f'0 {self.settings.currency}')`)
- `lbl_best_profile` (valeur `QLabel('-')`)
- `lbl_last_estimation` (valeur `QLabel('Dernière estimation : -')`)
- `figure` (valeur `Figure(figsize=(5, 2))`)
- `canvas` (valeur `FigureCanvasQTAgg(self.figure)`)
- `cost_figure` (valeur `Figure(figsize=(4, 2))`)
- `cost_canvas` (valeur `FigureCanvasQTAgg(self.cost_figure)`)
- `top_table` (valeur `QTableWidget()`)
- `table` (valeur `QTableWidget()`)

**Méthodes :**

- `__init__(self, estimation_repository, settings_service: SettingsService, parent) -> None`
- `_build_ui(self) -> None`
- `load_data(self) -> None`
- `_update_chart(self, reports) -> None`
- `_update_cost_chart(self, reports) -> None`
- `refresh(self) -> None`

### `ui.estimation_tab`

Fichier : `src\ui\estimation_tab.py`

**From imports :**

- `PyQt6.QtWidgets:QComboBox`
- `PyQt6.QtWidgets:QGridLayout`
- `PyQt6.QtWidgets:QGroupBox`
- `PyQt6.QtWidgets:QHBoxLayout`
- `PyQt6.QtWidgets:QLabel`
- `PyQt6.QtWidgets:QLineEdit`
- `PyQt6.QtWidgets:QMessageBox`
- `PyQt6.QtWidgets:QPushButton`
- `PyQt6.QtWidgets:QTextEdit`
- `PyQt6.QtWidgets:QVBoxLayout`
- `PyQt6.QtWidgets:QWidget`
- `src.services.estimation_service:EstimationService`
- `src.services.profile_service:ProfileService`
- `src.services.project_service:ProjectService`
- `src.services.scenario_service:ScenarioService`
- `src.services.settings_service:SettingsService`

#### Classes

##### `EstimationTab`

**Héritage :** `QWidget`

**Attributs d'instance :**

- `settings_service` (valeur `settings_service`)
- `settings` (valeur `self.settings_service.get()`)
- `estimation_service` (valeur `EstimationService()`)
- `profile_service` (valeur `ProfileService()`)
- `project_service` (valeur `ProjectService()`)
- `scenario_service` (valeur `ScenarioService()`)
- `profile_combo` (valeur `QComboBox()`)
- `project_combo` (valeur `QComboBox()`)
- `scenario_combo` (valeur `QComboBox()`)
- `estimate_button` (valeur `QPushButton("Calculer l'estimation")`)
- `hours_edit` (valeur `QLineEdit()`)
- `days_edit` (valeur `QLineEdit()`)
- `cost_edit` (valeur `QLineEdit()`)
- `cost_label` (valeur `QLabel(f'Coût estimé ({self.settings.currency})')`)
- `details_text` (valeur `QTextEdit()`)

**Méthodes :**

- `__init__(self, settings_service, parent) -> None`
- `_build_ui(self) -> None`
- `_load_data(self) -> None`
- `calculate_estimation(self) -> None`
- `_display_details(self, project, profile, scenario, result) -> None`
- `_update_labels(self) -> None`
- `refresh(self) -> None`

### `ui.main_window`

Fichier : `src\ui\main_window.py`

**From imports :**

- `PyQt6.QtGui:QAction`
- `PyQt6.QtWidgets:QMainWindow`
- `PyQt6.QtWidgets:QMessageBox`
- `PyQt6.QtWidgets:QTabWidget`
- `src.persistence.estimation_repository:EstimationRepository`
- `src.services.settings_service:SettingsService`
- `src.ui.dashboard_tab:DashboardTab`
- `src.ui.estimation_tab:EstimationTab`
- `src.ui.profiles_tab:ProfilesTab`
- `src.ui.projects_tab:ProjectsTab`
- `src.ui.reports_tab:ReportsTab`
- `src.ui.scenarios_tab:ScenariosTab`
- `src.ui.settings_dialog:SettingsDialog`

#### Classes

##### `MainWindow`

**Héritage :** `QMainWindow`

**Attributs d'instance :**

- `settings_service` (valeur `settings_service`)
- `settings` (valeur `self.settings_service.get()`)
- `estimation_repository` (valeur `EstimationRepository()`)
- `tabs` (valeur `QTabWidget()`)
- `projects_tab` (valeur `ProjectsTab()`)
- `profiles_tab` (valeur `ProfilesTab(self.settings_service)`)
- `estimation_tab` (valeur `EstimationTab(self.settings_service)`)
- `scenarios_tab` (valeur `ScenariosTab()`)
- `reports_tab` (valeur `ReportsTab(self.estimation_repository, self.settings_service)`)
- `dashboard_tab` (valeur `DashboardTab(self.estimation_repository, self.settings_service)`)

**Méthodes :**

- `__init__(self, settings_service: SettingsService) -> None`
- `_create_ui(self) -> None`
- `_create_menu(self) -> None`
- `_create_statusbar(self) -> None`
- `run_estimation(self) -> None`
- `show_about(self) -> None`
- `on_tab_changed(self, index) -> None`
- `show_settings(self) -> None`
- `reload_settings(self) -> None`
- `closeEvent(self, event) -> None`

### `ui.profile_dialog`

Fichier : `src\ui\profile_dialog.py`

**From imports :**

- `PyQt6.QtWidgets:QDialog`
- `PyQt6.QtWidgets:QDialogButtonBox`
- `PyQt6.QtWidgets:QDoubleSpinBox`
- `PyQt6.QtWidgets:QFormLayout`
- `PyQt6.QtWidgets:QGroupBox`
- `PyQt6.QtWidgets:QLineEdit`
- `PyQt6.QtWidgets:QTextEdit`
- `PyQt6.QtWidgets:QVBoxLayout`
- `src.models.user_profile:UserProfile`

#### Classes

##### `ProfileDialog`

**Héritage :** `QDialog`

**Attributs d'instance :**

- `profile` (valeur `profile`)
- `nom_edit` (valeur `QLineEdit()`)
- `description_edit` (valeur `QTextEdit()`)
- `taux_journalier_edit` (valeur `QDoubleSpinBox()`)
- `heures_par_jour_edit` (valeur `QDoubleSpinBox()`)
- `facteur_productivite_edit` (valeur `QDoubleSpinBox()`)
- `heure_par_ligne_edit` (valeur `self._create_time_spin()`)
- `heure_par_support_edit` (valeur `self._create_time_spin()`)
- `heure_par_vanne_edit` (valeur `self._create_time_spin()`)
- `heure_par_boite_a_ressort_edit` (valeur `self._create_time_spin()`)
- `heure_compensateur_edit` (valeur `self._create_time_spin()`)
- `heure_par_bride_edit` (valeur `self._create_time_spin()`)
- `heure_par_equipement_edit` (valeur `self._create_time_spin()`)

**Méthodes :**

- `__init__(self, parent, profile) -> None`
- `_build_ui(self) -> None`
- `_create_time_spin(self) -> None`
- `_load_profile(self) -> None`
- `get_profile(self) -> UserProfile`

### `ui.profiles_tab`

Fichier : `src\ui\profiles_tab.py`

**From imports :**

- `PyQt6.QtCore:Qt`
- `PyQt6.QtGui:QColor`
- `PyQt6.QtWidgets:QAbstractItemView`
- `PyQt6.QtWidgets:QHBoxLayout`
- `PyQt6.QtWidgets:QHeaderView`
- `PyQt6.QtWidgets:QLabel`
- `PyQt6.QtWidgets:QMessageBox`
- `PyQt6.QtWidgets:QPushButton`
- `PyQt6.QtWidgets:QTableWidget`
- `PyQt6.QtWidgets:QTableWidgetItem`
- `PyQt6.QtWidgets:QVBoxLayout`
- `PyQt6.QtWidgets:QWidget`
- `src.services.profile_service:ProfileService`
- `src.services.settings_service:SettingsService`
- `src.ui.profile_dialog:ProfileDialog`

#### Classes

##### `ProfilesTab`

**Héritage :** `QWidget`

**Attributs d'instance :**

- `settings_service` (valeur `settings_service`)
- `settings` (valeur `self.settings_service.get()`)
- `profile_service` (valeur `ProfileService()`)
- `profile_table` (valeur `QTableWidget()`)
- `details_label` (valeur `QLabel('Sélectionnez un profil.')`)
- `btn_add` (valeur `QPushButton('Ajouter')`)
- `btn_edit` (valeur `QPushButton('Modifier')`)
- `btn_delete` (valeur `QPushButton('Supprimer')`)
- `btn_refresh` (valeur `QPushButton('Actualiser')`)

**Méthodes :**

- `__init__(self, settings_service, parent) -> None`
- `_build_ui(self) -> None`
- `load_profiles(self) -> None`
- `on_profile_selected(self) -> None`
- `add_profile(self) -> None`
- `edit_profile(self) -> None`
- `delete_profile(self) -> None`
- `get_selected_profile(self) -> None`
- `_update_labels(self) -> None`
- `refresh(self) -> None`

### `ui.project_dialog`

Fichier : `src\ui\project_dialog.py`

**From imports :**

- `PyQt6.QtWidgets:QDialog`
- `PyQt6.QtWidgets:QDialogButtonBox`
- `PyQt6.QtWidgets:QFormLayout`
- `PyQt6.QtWidgets:QGroupBox`
- `PyQt6.QtWidgets:QLineEdit`
- `PyQt6.QtWidgets:QSpinBox`
- `PyQt6.QtWidgets:QTextEdit`
- `PyQt6.QtWidgets:QVBoxLayout`
- `src.models.deliverables:Deliverables`
- `src.models.project:Project`
- `src.models.project_parameters:ProjectParameters`
- `src.models.review_metrics:ReviewMetrics`

#### Classes

##### `ProjectDialog`

**Héritage :** `QDialog`

**Attributs d'instance :**

- `project` (valeur `project`)
- `nom_edit` (valeur `QLineEdit()`)
- `client_edit` (valeur `QLineEdit()`)
- `description_edit` (valeur `QTextEdit()`)
- `nb_lignes_edit` (valeur `QSpinBox()`)
- `nb_supports_edit` (valeur `QSpinBox()`)
- `nb_vannes_edit` (valeur `QSpinBox()`)
- `nb_brides_edit` (valeur `QSpinBox()`)
- `nb_compensateur_edit` (valeur `QSpinBox()`)
- `nb_connexions_edit` (valeur `QSpinBox()`)
- `nb_soudures_edit` (valeur `QSpinBox()`)
- `rapport_calcul_edit` (valeur `QSpinBox()`)
- `rapport_inter_edit` (valeur `QSpinBox()`)
- `notes_supports_edit` (valeur `QSpinBox()`)
- `notes_equipements_edit` (valeur `QSpinBox()`)
- `plans_supports_edit` (valeur `QSpinBox()`)
- `presentation_client_edit` (valeur `QSpinBox()`)
- `fichier_modele_edit` (valeur `QSpinBox()`)
- `fichier_resultat_edit` (valeur `QSpinBox()`)
- `revues_internes_edit` (valeur `QSpinBox()`)
- `revues_client_edit` (valeur `QSpinBox()`)
- `aller_retour_edit` (valeur `QSpinBox()`)

**Méthodes :**

- `__init__(self, project, parent) -> None`
- `_build_ui(self) -> None`
- `_load_project(self) -> None`
- `get_project(self) -> None`

### `ui.projects_tab`

Fichier : `src\ui\projects_tab.py`

**From imports :**

- `PyQt6.QtCore:Qt`
- `PyQt6.QtWidgets:QHBoxLayout`
- `PyQt6.QtWidgets:QHeaderView`
- `PyQt6.QtWidgets:QLabel`
- `PyQt6.QtWidgets:QMessageBox`
- `PyQt6.QtWidgets:QPushButton`
- `PyQt6.QtWidgets:QTableWidget`
- `PyQt6.QtWidgets:QTableWidgetItem`
- `PyQt6.QtWidgets:QVBoxLayout`
- `PyQt6.QtWidgets:QWidget`
- `src.services.project_service:ProjectService`
- `src.ui.project_dialog:ProjectDialog`

#### Classes

##### `ProjectsTab`

**Héritage :** `QWidget`

**Attributs d'instance :**

- `project_service` (valeur `ProjectService()`)
- `btn_new` (valeur `QPushButton('Nouveau')`)
- `btn_edit` (valeur `QPushButton('Modifier')`)
- `btn_delete` (valeur `QPushButton('Supprimer')`)
- `btn_refresh` (valeur `QPushButton('Actualiser')`)
- `table` (valeur `QTableWidget()`)
- `details_label` (valeur `QLabel('Sélectionnez un projet.')`)

**Méthodes :**

- `__init__(self, parent) -> None`
- `_build_ui(self) -> None`
- `load_projects(self) -> None`
- `get_selected_project(self) -> None`
- `create_project(self) -> None`
- `edit_project(self) -> None`
- `delete_project(self) -> None`
- `on_project_selected(self) -> None`
- `refresh(self) -> None`

### `ui.reports_tab`

Fichier : `src\ui\reports_tab.py`

**Imports :**

- `os`
- `subprocess`

**From imports :**

- `PyQt6.QtCore:Qt`
- `PyQt6.QtWidgets:QAbstractItemView`
- `PyQt6.QtWidgets:QFormLayout`
- `PyQt6.QtWidgets:QGroupBox`
- `PyQt6.QtWidgets:QHBoxLayout`
- `PyQt6.QtWidgets:QInputDialog`
- `PyQt6.QtWidgets:QLabel`
- `PyQt6.QtWidgets:QMessageBox`
- `PyQt6.QtWidgets:QPushButton`
- `PyQt6.QtWidgets:QTableWidget`
- `PyQt6.QtWidgets:QTableWidgetItem`
- `PyQt6.QtWidgets:QVBoxLayout`
- `PyQt6.QtWidgets:QWidget`
- `pathlib:Path`
- `src.services.excel_export_service:ExcelExportService`
- `src.services.pdf_export_service:PdfExportService`
- `src.services.settings_service:SettingsService`

#### Classes

##### `NumericTableWidgetItem`

**Héritage :** `QTableWidgetItem`

**Méthodes :**

- `__lt__(self, other) -> None`

##### `ReportsTab`

**Héritage :** `QWidget`

**Attributs d'instance :**

- `estimation_repository` (valeur `estimation_repository`)
- `settings_service` (valeur `settings_service`)
- `settings` (valeur `self.settings_service.get()`)
- `pdf_export_service` (valeur `PdfExportService()`)
- `excel_export_service` (valeur `ExcelExportService()`)
- `reports_table` (valeur `QTableWidget()`)
- `open_btn` (valeur `QPushButton('Ouvrir')`)
- `rename_btn` (valeur `QPushButton('Renommer')`)
- `delete_btn` (valeur `QPushButton('Supprimer')`)
- `refresh_btn` (valeur `QPushButton('Actualiser')`)
- `open_exports_btn` (valeur `QPushButton('Ouvrir exports')`)
- `pdf_btn` (valeur `QPushButton('Exporter PDF')`)
- `excel_btn` (valeur `QPushButton('Exporter Excel')`)
- `lbl_name` (valeur `QLabel('-')`)
- `lbl_project` (valeur `QLabel('-')`)
- `lbl_scenario` (valeur `QLabel('-')`)
- `lbl_budget` (valeur `QLabel('-')`)
- `lbl_date` (valeur `QLabel('-')`)

**Méthodes :**

- `__init__(self, estimation_repository, settings_service: SettingsService, parent) -> None`
- `_build_ui(self) -> None`
- `load_reports(self) -> None`
- `_get_selected_report(self) -> None`
- `_update_details(self) -> None`
- `_open_report(self) -> None`
- `rename_report(self) -> None`
- `delete_report(self) -> None`
- `export_pdf(self) -> None`
- `export_excel(self) -> None`
- `open_exports_folder(self) -> None`

### `ui.scenario_dialog`

Fichier : `src\ui\scenario_dialog.py`

**From imports :**

- `PyQt6.QtWidgets:QCheckBox`
- `PyQt6.QtWidgets:QDialog`
- `PyQt6.QtWidgets:QDialogButtonBox`
- `PyQt6.QtWidgets:QDoubleSpinBox`
- `PyQt6.QtWidgets:QFormLayout`
- `PyQt6.QtWidgets:QGroupBox`
- `PyQt6.QtWidgets:QLineEdit`
- `PyQt6.QtWidgets:QTextEdit`
- `PyQt6.QtWidgets:QVBoxLayout`
- `src.models.scenario:Scenario`

#### Classes

##### `ScenarioDialog`

**Héritage :** `QDialog`

**Attributs d'instance :**

- `scenario` (valeur `scenario`)
- `nom_edit` (valeur `QLineEdit()`)
- `description_edit` (valeur `QTextEdit()`)
- `productivite_edit` (valeur `QDoubleSpinBox()`)
- `risque_edit` (valeur `QDoubleSpinBox()`)
- `disponibilite_edit` (valeur `QDoubleSpinBox()`)
- `actif_check` (valeur `QCheckBox()`)

**Méthodes :**

- `__init__(self, parent, scenario) -> None`
- `_build_ui(self) -> None`
- `_load_scenario(self) -> None`
- `get_scenario(self) -> Scenario`

### `ui.scenarios_tab`

Fichier : `src\ui\scenarios_tab.py`

**From imports :**

- `PyQt6.QtCore:Qt`
- `PyQt6.QtWidgets:QGroupBox`
- `PyQt6.QtWidgets:QHBoxLayout`
- `PyQt6.QtWidgets:QMessageBox`
- `PyQt6.QtWidgets:QPushButton`
- `PyQt6.QtWidgets:QTableWidget`
- `PyQt6.QtWidgets:QTableWidgetItem`
- `PyQt6.QtWidgets:QTextEdit`
- `PyQt6.QtWidgets:QVBoxLayout`
- `PyQt6.QtWidgets:QWidget`
- `src.services.scenario_service:ScenarioService`
- `src.ui.scenario_dialog:ScenarioDialog`

#### Classes

##### `ScenariosTab`

**Héritage :** `QWidget`

**Attributs d'instance :**

- `service` (valeur `ScenarioService()`)
- `add_button` (valeur `QPushButton('Ajouter')`)
- `edit_button` (valeur `QPushButton('Modifier')`)
- `delete_button` (valeur `QPushButton('Supprimer')`)
- `refresh_button` (valeur `QPushButton('Rafraîchir')`)
- `table` (valeur `QTableWidget()`)
- `details_text` (valeur `QTextEdit()`)
- `scenarios` (valeur `self.service.get_all_scenarios()`)

**Méthodes :**

- `__init__(self, parent) -> None`
- `_build_ui(self) -> None`
- `load_scenarios(self) -> None`
- `get_selected_scenario(self) -> None`
- `add_scenario(self) -> None`
- `edit_scenario(self) -> None`
- `delete_scenario(self) -> None`
- `_show_details(self) -> None`
- `refresh(self) -> None`

### `ui.settings_dialog`

Fichier : `src\ui\settings_dialog.py`

**From imports :**

- `PyQt6.QtWidgets:QCheckBox`
- `PyQt6.QtWidgets:QComboBox`
- `PyQt6.QtWidgets:QDialog`
- `PyQt6.QtWidgets:QDialogButtonBox`
- `PyQt6.QtWidgets:QDoubleSpinBox`
- `PyQt6.QtWidgets:QFormLayout`
- `PyQt6.QtWidgets:QLineEdit`
- `PyQt6.QtWidgets:QMessageBox`
- `PyQt6.QtWidgets:QSpinBox`
- `PyQt6.QtWidgets:QTabWidget`
- `PyQt6.QtWidgets:QVBoxLayout`
- `PyQt6.QtWidgets:QWidget`
- `src.models.app_settings:AppSettings`
- `src.services.settings_service:SettingsService`

#### Classes

##### `SettingsDialog`

**Héritage :** `QDialog`

**Attributs d'instance :**

- `settings_service` (valeur `settings_service`)
- `settings` (valeur `self.settings_service.get()`)
- `tabs` (valeur `QTabWidget()`)
- `company_edit` (valeur `QLineEdit()`)
- `currency_combo` (valeur `QComboBox()`)
- `export_directory_edit` (valeur `QLineEdit()`)
- `hours_per_day_spin` (valeur `QDoubleSpinBox()`)
- `days_per_month_spin` (valeur `QSpinBox()`)
- `theme_combo` (valeur `QComboBox()`)
- `font_size_spin` (valeur `QSpinBox()`)
- `dashboard_kpis_check` (valeur `QCheckBox('Afficher les KPI Dashboard')`)
- `dashboard_charts_check` (valeur `QCheckBox('Afficher les graphiques Dashboard')`)
- `buttons` (valeur `QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)`)

**Méthodes :**

- `__init__(self, settings_service: SettingsService, parent) -> None`
- `_create_ui(self) -> None`
- `_load_settings(self) -> None`
- `_save(self) -> None`

### `utils.exceptions`

Fichier : `src\utils\exceptions.py`

#### Classes

##### `EstimateFlexError`

**Héritage :** `Exception`

##### `ValidationError`

**Héritage :** `EstimateFlexError`

##### `DatabaseError`

**Héritage :** `EstimateFlexError`

##### `EstimationError`

**Héritage :** `EstimateFlexError`

##### `ReportGenerationError`

**Héritage :** `EstimateFlexError`

### `utils.string_utils`

Fichier : `src\utils\string_utils.py`

**Imports :**

- `re`
- `unicodedata`

#### Fonctions top-level

- `normalize_name(value: str) -> str`

## Relations entre classes

### Héritage

- `DatabaseError` hérite de `EstimateFlexError`
- `EstimationError` hérite de `EstimateFlexError`
- `ReportGenerationError` hérite de `EstimateFlexError`
- `ValidationError` hérite de `EstimateFlexError`

### Composition

- Aucune.

### Dépendances

- `CostEngine` dépend de `CostBreakdown`
- `DashboardTab` dépend de `SettingsService`
- `DurationEngine` dépend de `DurationBreakdown`
- `EstimationRepository` dépend de `EstimationResult`
- `EstimationService` dépend de `EstimationRepository`
- `EstimationService` dépend de `EstimationResult`
- `EstimationService` dépend de `Estimator`
- `EstimationService` dépend de `Project`
- `EstimationService` dépend de `Scenario`
- `EstimationService` dépend de `UserProfile`
- `EstimationTab` dépend de `EstimationService`
- `EstimationTab` dépend de `ProfileService`
- `EstimationTab` dépend de `ProjectService`
- `EstimationTab` dépend de `ScenarioService`
- `Estimator` dépend de `CostEngine`
- `Estimator` dépend de `DurationEngine`
- `Estimator` dépend de `EstimationResult`
- `Estimator` dépend de `Project`
- `Estimator` dépend de `RiskEngine`
- `Estimator` dépend de `UserProfile`
- `MainWindow` dépend de `DashboardTab`
- `MainWindow` dépend de `EstimationRepository`
- `MainWindow` dépend de `EstimationTab`
- `MainWindow` dépend de `ProfilesTab`
- `MainWindow` dépend de `ProjectsTab`
- `MainWindow` dépend de `ReportsTab`
- `MainWindow` dépend de `ScenariosTab`
- `MainWindow` dépend de `SettingsDialog`
- `MainWindow` dépend de `SettingsService`
- `ProfileDialog` dépend de `UserProfile`
- `ProfileRepository` dépend de `UserProfile`
- `ProfileService` dépend de `ProfileRepository`
- `ProfileService` dépend de `UserProfile`
- `ProfilesTab` dépend de `ProfileDialog`
- `ProfilesTab` dépend de `ProfileService`
- `ProjectDialog` dépend de `Deliverables`
- `ProjectDialog` dépend de `Project`
- `ProjectDialog` dépend de `ProjectParameters`
- `ProjectDialog` dépend de `ReviewMetrics`
- `ProjectRepository` dépend de `Deliverables`
- `ProjectRepository` dépend de `Project`
- `ProjectRepository` dépend de `ProjectParameters`
- `ProjectRepository` dépend de `ReviewMetrics`
- `ProjectService` dépend de `Project`
- `ProjectService` dépend de `ProjectRepository`
- `ProjectService` dépend de `ValidationError`
- `ProjectsTab` dépend de `ProjectDialog`
- `ProjectsTab` dépend de `ProjectService`
- `ReportsTab` dépend de `ExcelExportService`
- `ReportsTab` dépend de `NumericTableWidgetItem`
- `ReportsTab` dépend de `PdfExportService`
- `ReportsTab` dépend de `SettingsService`
- `RiskEngine` dépend de `RiskResult`
- `ScenarioDialog` dépend de `Scenario`
- `ScenarioEngine` dépend de `ScenarioResult`
- `ScenarioEngine` dépend de `ScenarioType`
- `ScenarioRepository` dépend de `Scenario`
- `ScenarioService` dépend de `Scenario`
- `ScenarioService` dépend de `ScenarioRepository`
- `ScenariosTab` dépend de `ScenarioDialog`
- `ScenariosTab` dépend de `ScenarioService`
- `SettingsDialog` dépend de `AppSettings`
- `SettingsDialog` dépend de `SettingsService`
- `SettingsRepository` dépend de `AppSettings`
- `SettingsService` dépend de `AppSettings`
- `SettingsService` dépend de `SettingsRepository`

## Fichiers générés

- `architecture_report.md` — rapport complet
- `architecture.json` — représentation structurée
- `diagrams/modules.mmd` — diagramme Mermaid des modules
- `diagrams/modules.svg` — diagramme SVG des modules
- `diagrams/classes.mmd` — diagramme Mermaid des classes
- `diagrams/classes.svg` — diagramme SVG des classes
