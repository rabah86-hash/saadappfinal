import flet as ft
import json

MUNICIPALITIES = [
    "تيسمسيلت", "أولاد بسام", "خميستي", "العيون", "ثنية الحد",
    "سيدي بوتشنت", "لرجام", "ملعب", "سيدي عابد", "تملاحت",
    "برج بونعامة", "بني شعيب", "بني لحسن", "سيدي سليمان",
    "عماري", "معصم", "الأزهرية", "بوقايد", "الأربعاء",
    "برج الأمير عبد القادر", "اليوسفية", "سيدي العنتري"
]

def main(page: ft.Page):
    page.title = "دعم ساعد ولد قدور"
    page.rtl = True
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    name_field = ft.TextField(
        label="الاسم واللقب",
        width=350
    )

    municipality = ft.Dropdown(
        label="البلدية",
        width=350,
        options=[ft.dropdown.Option(x) for x in MUNICIPALITIES]
    )

    stats = ft.Column()
    voters = ft.Column(width=400)

    def load_data():
        try:
            data = page.client_storage.get("supporters")
            if data:
                return json.loads(data)
            return []
        except:
            return []

    def save_data(data):
        page.client_storage.set(
            "supporters",
            json.dumps(data, ensure_ascii=False)
        )

    def show_message(text):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(text)
        )
        page.snack_bar.open = True
        page.update()

    def delete_voter(index):
        data = load_data()

        if index < len(data):
            data.pop(index)

        save_data(data)
        refresh()
        show_message("تم الحذف بنجاح")

    def add_voter(e):
        if not name_field.value:
            show_message("أدخل الاسم واللقب")
            return

        if not municipality.value:
            show_message("اختر البلدية")
            return

        data = load_data()

        data.append({
            "name": name_field.value,
            "mun": municipality.value
        })

        save_data(data)

        name_field.value = ""
        municipality.value = None

        refresh()
        show_message("تمت الإضافة بنجاح")

    def refresh():
        data = load_data()

        stats.controls.clear()
        voters.controls.clear()

        stats.controls.append(
            ft.Text(
                f"إجمالي المؤيدين: {len(data)}",
                size=20,
                weight=ft.FontWeight.BOLD
            )
        )

        count = {}

        for item in data:
            mun = item["mun"]
            count[mun] = count.get(mun, 0) + 1

        for mun, total in count.items():
            stats.controls.append(
                ft.Text(f"{mun}: {total}")
            )

        for i, item in reversed(list(enumerate(data))):
            voters.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                ft.Text(
                                    f"{item['name']} - {item['mun']}",
                                    expand=True
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="red",
                                    on_click=lambda e, idx=i: delete_voter(idx)
                                )
                            ]
                        )
                    )
                )
            )

        page.update()

    page.add(
        ft.Text(
            "دعم ساعد ولد قدور",
            size=24,
            weight=ft.FontWeight.BOLD
        ),

        ft.Divider(),

        name_field,
        municipality,

        ft.ElevatedButton(
            "إضافة مؤيد",
            icon=ft.Icons.ADD,
            width=350,
            on_click=add_voter
        ),

        ft.Divider(),

        stats,

        ft.Divider(),

        ft.Text(
            "قائمة المؤيدين",
            size=18,
            weight=ft.FontWeight.BOLD
        ),

        voters,

        ft.Divider(),

        ft.Text(
            "تم التطوير من طرف الأستاذ: بارد رابح",
            size=12
        ),

        ft.Text(
            "اللهم ارحم والدي واغفر لهما كما ربياني صغيراً",
            size=12
        )
    )

    refresh()

if __name__ == "__main__":
    ft.run(main)