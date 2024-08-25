import json
import flet as ft


#345 - продолжить , нужен фикс

#Основная страница приложения
async def main(page: ft.Page):
    #Настройки приложения по умолчанию
    page.title = "JustBuy"
    page.theme_mode = "light"

    #Username текущего пользователя
    global local_username
    local_username = ""


    #Функция для смены страниц
    async def route_change(route):
        page.views.clear()

        messages = ft.Column(
            controls=[ft.Text("Welcome to your messanger!")],
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )

        with open("messages.json", "r") as file:
            data = json.load(file)
        for i in data["messages"]:
            messages.controls.append(ft.Text(i.get("Author") + ": " + i.get("Content")))
        page.update()

        def send_message(event):
            with open("messages.json", "r") as file:
                data = json.load(file)
            data["messages"].append({"Author": name_field.value, "Content": input_field.value})
            with open("messages.json", "w") as file:
                json.dump(data, file)

            messages.controls.clear()
            for i in data["messages"]:
                messages.controls.append(ft.Text(i.get("Author") + ": " + i.get("Content")))

            page.update()

        name_field = ft.TextField(
            hint_text="Your name"
        )
        input_field = ft.TextField(
            hint_text="Your message"
        )
        send_button = ft.IconButton(icon=ft.icons.SEND, on_click=send_message)

        row = ft.Row(
            controls=[input_field, send_button]
        )


        #Привествесвенная страница
        if page.route == "/home":
            page.views.append(
                ft.View(
                    route='/home',
                    controls=[
                        ft.Text("Messages"),
                        name_field,
                        row,
                        messages
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START
                )
            )
            page.update()



        await page.update_async()


    #Анимация перехода между страницами
    async def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    #Переход на привественную страницу при запуске приложения
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async('/home')

#Запуск приложения
ft.app(target=main, assets_dir='assets')