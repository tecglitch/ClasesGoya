import csv
import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Project, Task

logger = logging.getLogger(__name__)
DATA_DIR = settings.BASE_DIR / "data"


class Command(BaseCommand):
    help = "Importa tareas desde proveedores JSON, CSV y XML"

    def handle(self, *args, **options):
        log_path = settings.BASE_DIR / "import.log"
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            encoding="utf-8",
        )
        total = 0
        total += self._import_json("tasks_provider_a.json", "proveedor_a")
        total += self._import_csv("tasks_provider_b.csv", "proveedor_b")
        total += self._import_xml("tasks_provider_c.xml", "proveedor_c")
        total += self._import_json("tasks_provider_d.json", "proveedor_d")
        self.stdout.write(self.style.SUCCESS(f"Importación finalizada: {total} tareas cargadas"))
        self.stdout.write(f"Log de importación: {log_path.name}")

    def _report(self, message, *, warning=False):
        if warning:
            logger.warning(message)
            self.stdout.write(self.style.WARNING(message))
        else:
            logger.error(message)
            self.stderr.write(self.style.ERROR(message))

    def _import_json(self, filename, source):
        path = DATA_DIR / filename
        try:
            with path.open(encoding="utf-8-sig") as stream:
                data = json.load(stream)
            if not isinstance(data, list):
                raise ValueError("el documento debe contener una lista")
        except (OSError, json.JSONDecodeError, ValueError) as error:
            self._report(f"Error importando {path.name}: {error}")
            return 0
        return self._import_items(data, source)

    def _import_csv(self, filename, source):
        path = DATA_DIR / filename
        try:
            with path.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.DictReader(stream))
        except OSError as error:
            self._report(f"Error importando {path.name}: {error}")
            return 0
        return self._import_items(rows, source)

    def _import_xml(self, filename, source):
        path = DATA_DIR / filename
        try:
            root = ET.parse(path).getroot()
        except (OSError, ET.ParseError) as error:
            self._report(f"Error importando {path.name}: {error}")
            return 0
        rows = []
        for element in root.findall("task"):
            rows.append({
                key: (element.findtext(key) or "").strip()
                for key in ("title", "priority", "status")
            })
        return self._import_items(rows, source)

    def _import_items(self, rows, source):
        count = 0
        project, _ = Project.objects.get_or_create(
            name=f"Importación {source.replace('_', ' ').title()}"
        )
        for item in rows:
            if not isinstance(item, dict) or not str(item.get("title", "")).strip():
                self._report(f"[{source}] Item sin título, se ignora", warning=True)
                continue
            title = str(item["title"]).strip()
            _, created = Task.objects.get_or_create(
                title=title,
                project=project,
                defaults={
                    "project": project,
                    "priority": item.get("priority") or "media",
                    "status": item.get("status") or "pendiente",
                },
            )
            count += int(created)
        return count
