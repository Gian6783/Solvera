import flet as ft
from solver_core import SolveraEngine

# Initialisation du moteur d'IA
engine = SolveraEngine()

def app_main(page: ft.Page):
    page.title = "SOLVERA"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.favicon = "icon.png"  # <--- Ajout de l'icône pour le web

    # Historique propre à chaque utilisateur (totalement isolé et privé)
    history_data = []
    
    chat_history = ft.ListView(expand=True, spacing=15, padding=20, auto_scroll=True)

    def create_message_bubble(text, is_user=True):
        prefix = "Vous : " if is_user else "Solvera : "
        alignment = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        
        return ft.Row(
            [
                ft.Container(
                    content=ft.Text(
                        f"{prefix}{text}",
                        selectable=True,
                    ),
                    width=320,
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.Colors.GREY_900 if not is_user else ft.Colors.BLUE_900,
                )
            ],
            alignment=alignment
        )

    def send_message(e):
        user_text = prompt_input.value.strip()
        if not user_text:
            return
        
        prompt_input.value = ""
        chat_history.controls.append(create_message_bubble(user_text, is_user=True))
        page.update()

        history_data.append({"role": "user", "text": user_text})

        # Gestion de l'historique récent pour le contexte textuel
        recent_history = history_data[-6:]
        context_prompt = "Voici l'historique récent de notre conversation pour mémoire :\n"
        for item in recent_history:
            role = "Moi" if item["role"] == "user" else "Solvera"
            context_prompt += f"- {role} : {item['text']}\n"
        
        context_prompt += f"\nMaintenant, réponds à cette nouvelle question/problème : {user_text}"

        try:
            response_text = engine.process_command(prompt=context_prompt)
        except Exception as err:
            response_text = f"Erreur de traitement : {err}"

        chat_history.controls.append(create_message_bubble(response_text, is_user=False))
        page.update()

        history_data.append({"role": "assistant", "text": response_text})

    prompt_input = ft.TextField(
        hint_text="Décrivez votre problème...",
        expand=True,
        border_radius=20,
        on_submit=send_message
    )

    send_btn = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color="blue_400",
        on_click=send_message
    )

    input_bar = ft.Container(
        content=ft.Row([prompt_input, send_btn], alignment=ft.MainAxisAlignment.CENTER),
        padding=10
    )

    legal_footer = ft.Container(
        content=ft.Column([
            ft.Text(
                "Solvera est une IA, elle peut se tromper dans ses réponses. Veuillez vérifier les réponses.",
                size=11,
                color=ft.Colors.GREY_400,
                text_align=ft.TextAlign.CENTER
            ),
            ft.TextButton(
                content=ft.Text("Politique de confidentialité"),
                url="https://example.com/confidentialite",
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        padding=10
    )

    page.add(
        ft.SafeArea(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("SOLVERA", size=24, weight=ft.FontWeight.BOLD, color="blue_400"),
                    padding=20
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                chat_history,
                legal_footer,
                input_bar
            ], expand=True),
            expand=True
        )
    )

# Lancement de l'application avec la prise en compte du dossier assets
if __name__ == "__main__":
    ft.app(target=app_main, assets_dir="assets")