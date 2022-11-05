class RoadMapDict:
    roadmap_dict = {}

    def __init__(self) -> None:
        self.roadmap_dict["recommended_height"] = 0

    def update_recommended_height(self, height):
        self.roadmap_dict["recommended_height"] = height

    def set_title_coordinates(self, x, y, width, height, title_text):
        self.roadmap_dict["title"] = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "text": title_text,
        }
        self.update_recommended_height(y + height)

    def set_timeline_coordinates(self, x, y, width, height):
        (
            current_x_pos,
            current_y_pos,
            current_width,
            current_height,
        ) = self.get_timeline_coordinates()

        if current_x_pos < x:
            current_x_pos = x
        if current_y_pos < y:
            current_y_pos = y
        if current_width < x + width:
            current_width = x + width
        if current_height < height:
            current_height = height

        if self.roadmap_dict.get("timeline", None) == None:
            self.roadmap_dict["timeline"] = {
                "x": current_x_pos,
                "y": current_y_pos,
                "width": current_width,
                "height": current_height,
                "timeline_items": {},
            }
        else:
            self.roadmap_dict["timeline"]["width"] = current_width
            self.roadmap_dict["timeline"]["height"] = current_height

        self.update_recommended_height(current_y_pos + current_height)

    def set_timeline_item_coordinates(self, item_id, x, y, width, height):
        self.set_timeline_coordinates(x, y, width, height)

        item = {"x": x, "y": y, "width": width, "height": height}

        self.roadmap_dict["timeline"]["timeline_items"][item_id] = item

    def get_timeline_item_text(self, item_id):
        return self.roadmap_dict["timeline"]["timeline_items"][item_id]["text"]

    def set_timeline_item_text(self, item_id, text):
        self.roadmap_dict["timeline"]["timeline_items"][item_id]["text"] = text

    def get_timeline_item_value(self, item_id):
        return self.roadmap_dict["timeline"]["timeline_items"][item_id]["value"]

    def set_timeline_item_value(self, item_id, value):
        self.roadmap_dict["timeline"]["timeline_items"][item_id]["value"] = value

    def get_timeline_item_coordinates(self, item_id):
        return (
            self.roadmap_dict["timeline"]["timeline_items"][item_id]["x"],
            self.roadmap_dict["timeline"]["timeline_items"][item_id]["y"],
            self.roadmap_dict["timeline"]["timeline_items"][item_id]["width"],
            self.roadmap_dict["timeline"]["timeline_items"][item_id]["height"],
        )

    def set_groups_coordinates(self, x, y, width, height):
        (
            current_x_pos,
            current_y_pos,
            current_width,
            current_height,
        ) = self.get_groups_coordinates()
        if current_x_pos < x:
            current_x_pos = x
        if current_y_pos < y:
            current_y_pos = y
        if current_width < x + width:
            current_width = x + width
        if current_height < height:
            current_height = height

        if self.roadmap_dict.get("groups", {}).get("x", 0) == 0:
            self.roadmap_dict["groups"] = {
                "x": x,
                "y": y,
                "group_items": {},
            }

        self.update_recommended_height(y + height)

    def set_groups_item_coordinates(self, item_id, x, y, width, height):
        self.set_groups_coordinates(x, y, width, height)
        current_x = 0
        current_y = 0
        current_width = 0
        current_height = 0
        (
            current_x,
            current_y,
            current_width,
            current_height,
        ) = self.get_groups_item_coordinates(item_id)
        if current_x < x:
            current_x = x
        if current_y < y:
            current_y = y
        if current_width < x + width:
            current_width = x + width
        if current_height < height:
            current_height = y + height

        if self.roadmap_dict["groups"]["group_items"].get(item_id, None) == None:
            self.roadmap_dict["groups"]["group_items"][item_id] = {
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "tasks": {},
            }
        else:
            self.roadmap_dict["groups"]["group_items"][item_id]["width"] = x + width
            self.roadmap_dict["groups"]["group_items"][item_id]["height"] = y + height

    def set_groups_item_task_coordinates(
        self, item_id, task_id, x, y, width, height, task_text
    ):

        self.set_groups_item_coordinates(item_id, x, y, width, height)

        self.roadmap_dict["groups"]["group_items"][item_id]["tasks"][task_id] = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "text": task_text,
        }

    def set_footer_coordinates(self, x, y, width, height):
        self.roadmap_dict["footer"] = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
        }
        self.roadmap_dict["recommended_height"] = y + height

    def get_recommended_height(self):
        return self.roadmap_dict.get("recommended_height", 0)

    def get_title_coordinates(self):
        return (
            self.roadmap_dict.get("title", "").get("x", 0),
            self.roadmap_dict.get("title", "").get("y", 0),
            self.roadmap_dict.get("title", "").get("width", 0),
            self.roadmap_dict.get("title", "").get("height", 0),
        )

    def get_timeline_coordinates(self):
        return (
            self.roadmap_dict.get("timeline", {}).get("x", 0),
            self.roadmap_dict.get("timeline", {}).get("y", 0),
            self.roadmap_dict.get("timeline", {}).get("width", 0),
            self.roadmap_dict.get("timeline", {}).get("height", 0),
        )

    def get_timeline_item_coordinates(self, item):
        return (
            self.roadmap_dict.get("timeline", {})
            .get("timeline_items", {})
            .get(item, {})
            .get("x", 0),
            self.roadmap_dict.get("timeline", {})
            .get("timeline_items", {})
            .get(item, {})
            .get("y", 0),
            self.roadmap_dict.get("timeline", {})
            .get("timeline_items", {})
            .get(item, {})
            .get("width", 0),
            self.roadmap_dict.get("timeline", {})
            .get("timeline_items", {})
            .get(item, {})
            .get("height", 0),
        )

    def get_timeline_item_text(self, item):
        return self.roadmap_dict.get("timeline", {}).get("timeline_items", {}).get(
            item, {}
        ).get("text", ""), self.roadmap_dict.get("timeline", {}).get(
            "timeline_items", {}
        ).get(
            item, {}
        ).get(
            "value", ""
        )

    def get_timeline_item_value(self, item):
        return (
            self.roadmap_dict.get("timeline", {})
            .get("timeline_items", {})
            .get(item, {})
            .get("value", "")
        )

    def get_groups_coordinates(self):
        return (
            self.roadmap_dict.get("groups", {}).get("x", 0),
            self.roadmap_dict.get("groups", {}).get("y", 0),
            self.roadmap_dict.get("groups", {}).get("width", 0),
            self.roadmap_dict.get("groups", {}).get("height", 0),
        )

    def get_groups_item_coordinates(self, item_id):
        x, y, width, height = 0, 0, 0, 0
        x = (
            self.roadmap_dict.get("groups", {})
            .get("group_items", {})
            .get(item_id, {})
            .get("x", 0)
        )
        y = (
            self.roadmap_dict.get("groups", {})
            .get("group_items", {})
            .get(item_id, {})
            .get("y", 0)
        )
        width = (
            self.roadmap_dict.get("groups", {})
            .get("group_items", {})
            .get(item_id, {})
            .get("width", 0)
        )
        height = (
            self.roadmap_dict.get("groups", {})
            .get("group_items", {})
            .get(item_id, {})
            .get("height", 0)
        )
        return (x, y, width, height)

    def get_groups_item_task_coordinates(self, item, task):
        return (
            self.roadmap_dict.get("groups", {})
            .get("group_items", {})
            .get(item, {})
            .get("tasks", {})
            .get(task, 0)
            .get("x", 0),
            self.roadmap_dict.get("groups", {})
            .get("group_items", {})
            .get(item, {})
            .get("tasks", {})
            .get(task, 0)
            .get("y", 0),
            self.roadmap_dict.get("groups", {})
            .get("group_items", {})
            .get(item, {})
            .get("tasks", {})
            .get(task, 0)
            .get("width", 0),
            self.roadmap_dict.get("groups", {})
            .get("group_items", {})
            .get(item, {})
            .get("tasks", {})
            .get(task, 0)
            .get("height", 0),
        )

    def get_footer_coordinates(self):
        return (
            self.roadmap_dict.get("footer", {}).get("x", 0),
            self.roadmap_dict.get("footer", {}).get("y", 0),
            self.roadmap_dict.get("footer", {}).get("width", 0),
            self.roadmap_dict.get("footer", {}).get("height", 0),
        )
