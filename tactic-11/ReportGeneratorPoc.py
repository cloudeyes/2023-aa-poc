from abc import ABC, abstractmethod


class Renderer(ABC):
    @abstractmethod
    def renderParagraph(self, paragraph):
        pass

    @abstractmethod
    def renderHeader(self, content):
        pass

    @abstractmethod
    def renderText(self, content):
        pass

    @abstractmethod
    def renderList(self, list):
        pass


class Renderable(ABC):
    @abstractmethod
    def accept(self, renderer: Renderer) -> str:
        pass


class Text(Renderable):
    def __init__(self, content: str):
        self.content = content

    def accept(self, renderer: Renderer) -> str:
        return renderer.renderText(self)


class Paragraph(Renderable):
    def __init__(self, content: str):
        self.content = content

    def accept(self, renderer: Renderer) -> str:
        return renderer.renderParagraph(self)


class Items(Renderable):
    def __init__(self, items: list[str]):
        self.items = items

    def accept(self, renderer: Renderer) -> str:
        return renderer.renderList(self)


class Header(Text):
    def __init__(self, content: str, depth=1):
        self.content = content
        self.depth = depth

    def accept(self, renderer: Renderer) -> str:
        return renderer.renderHeader(self)


class Section(Renderable):
    def __init__(self, *sections):
        self.items = list(sections)

    def accept(self, renderer: Renderer) -> str:
        return renderer.renderList(self)


class Document(Renderable):
    def __init__(self, *items: list[Renderable]):
        self.items = list(items)

    def accept(self, renderer: Renderer) -> str:
        output = ""
        for item in self.items:
            output += item.accept(renderer)
        return output


class Report(Renderable):
    def __init__(self, sections: list[Renderable]):
        self.sections = sections

    def accept(self, renderer: Renderer) -> str:
        output = ""
        for section in self.sections:
            output += section.accept(renderer)
        return output


class Section(Renderable):
    def __init__(self, title: str, *content: list[Renderable]):
        self.title = title
        self.content = list(content)

    def accept(self, renderer: Renderer) -> str:
        output = renderer.renderHeader(Header(self.title, 2))
        for c in self.content:
            output += c.accept(renderer)
        return output


report_plugin = plugin_manager.get_report_plugin()
renderer = report_plugin.get_renderer(format_type)
anomaly_report = get_anomaly_report(anomaly_session, report_template)
# Document(
#    Header("Anomaly Remedy Report"),
#    Section(
#        "Introduction",
#        Paragraph("This report summarizes ... "),
#    ),
#    ...,
# )

output = anomaly_report.accept(renderer)


class MarkdownRenderer(Renderer):
    def renderParagraph(self, paragraph: Paragraph) -> str:
        return f"{paragraph.content}\n\n"

    def renderHeader(self, content: Header) -> str:
        return f"{'#' * content.depth} {content.content}\n\n"

    def renderText(self, text: Text) -> str:
        return f"{text.content}"

    def renderList(self, list: Items) -> str:
        output = ""
        for item in list.items:
            output += f"- {item}\n"
        output += "\n"
        return output


class HtmlRenderer(Renderer):
    def renderParagraph(self, paragraph: Paragraph) -> str:
        return f"<p>{paragraph.content}</p>\n\n"

    def renderHeader(self, header: Header) -> str:
        return f"<h{header.depth}>{header.content}</h{header.depth}>\n\n"

    def renderText(self, text: Text) -> str:
        return f"{text.content}"

    def renderImage(self, image: "Image") -> str:
        return f'<img src="{image.url}" alt="{image.alt}" width="{image.width}" height="{image.height}" />\n'

    def renderList(self, lst: Items) -> str:
        items_html = "".join([f"<li>{self.render(item)}</li>" for item in lst.items])
        return f"<{lst.tag}>{items_html}</{lst.tag}>\n"


def main():
    import sys

    # Create the report structure using composite pattern
    format_type = sys.argv[1]
    anomaly_report = Document(
        Header("Anomaly Remedy Report"),
        Section(
            "Introduction",
            Paragraph(
                "This report summarizes the remedies for the anomalies that occurred in the manufacturing plants."
            ),
        ),
        Section(
            "Anomaly 1: Power Shortage",
            Paragraph("Remedy 1: Increase the capacity of the power supply."),
        ),
        Section(
            "Anomaly 2: Machine Malfunctioning",
            Paragraph("Remedy 1: Check and replace the malfunctioning parts."),
        ),
        Section(
            "Performance:",
            Paragraph("These remedies have been applied properly."),
        ),
    )

    if format_type == "html":
        # Render the report to HTML format using visitor pattern
        html_renderer = HtmlRenderer()
        output = anomaly_report.accept(html_renderer)
    elif format_type == "markdown":
        # Render the report to Markdown format using visitor pattern
        markdown_renderer = MarkdownRenderer()
        output = anomaly_report.accept(markdown_renderer)

    print(output)


if __name__ == "__main__":
    main()
