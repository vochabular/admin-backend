import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

from api.models import (
    Book,
    Chapter,
    ChapterTitle,
    Component,
    ComponentType,
    Translation,
    Text
)

"""
query {
  chapterXML(id: "d4cf7d34-c3f4-4e87-b452-6cd4923729b3") {
    path
  }
}
"""

class XMLGenerator():
    def createChapter(self, chapter):
        # Chapter header properties
        chapterElem = ET.Element("kapitel")
        ET.SubElement(chapterElem, "titel1_kapitel").text = "Kapitel"
        ET.SubElement(chapterElem, "titel1_zahl").text = str(chapter.number)
        # Chapter titles in languages
        titles = ChapterTitle.objects.filter(chapter=chapter)
        for title in titles:
            ET.SubElement(chapterElem, "titel1_inhalt_" +
                          title.language.id).text = title.title
        # Chapter description aka. lauftext
        ET.SubElement(chapterElem, "lauftext").text = chapter.description
        print("##################################################################")
        # Start listing components
        components = Component.objects.filter(
            fk_chapter=chapter).order_by("-order_in_chapter")
        for component in components:
            if component.fk_component:
                continue

            if component.fk_component_type.isTitle():
                title_component(component, chapterElem, "titel2_inhalt")

            if component.fk_component_type.isText():
                text_component(component, chapterElem)

            if component.fk_component_type.isDialogue():
                dialogue_component(component, chapterElem)

        tree = ET.ElementTree(chapterElem)
        xml = ET.tostring(tree.getroot())
        # print("\n\n")
        print(BeautifulSoup(xml, "xml").prettify())
        return xml


def title_component(component, elem, tag):
    texts = Text.objects.filter(fk_component=component)
    for text in texts:
        for translation in Translation.objects.filter(fk_text=text):
            if not translation.text_field:
                continue
            ET.SubElement(
                elem, tag + "_" + translation.fk_language.id).text = translation.text_field


def text_component(component, elem):
    texts = Text.objects.filter(fk_component=component)
    for text in texts:
        for translation in Translation.objects.filter(fk_text=text):
            if not translation.text_field:
                continue
            ET.SubElement(
                elem, "lauftext_" + translation.fk_language.id).text = translation.text_field


def dialogue_component(dialogue, elem):
    for component in Component.objects.filter(
            fk_component=dialogue).order_by("-order_in_chapter"):
        if component.fk_component_type.isTitle():
            title_component(component, elem, "titel2")

        if component.fk_component_type.isText():
            text_component(component, elem)

        if component.fk_component_type.isBubble():
            text_component(component, elem)
