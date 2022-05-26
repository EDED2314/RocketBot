import csv
import disnake


class csv_manager:
    def __init__(self):
        self.p = ['member', 'task', 'due', "channel", "message_id", 'dict']
        self.constants_p = ['guild_id', 'embed_id', 'embed_channel']

    async def organize(self):
        tasks = []
        r = csv.DictReader(open("tasks.csv", "r"))
        for row in r:
            tasks.append((row['member'], row['task'], row['due']))
        return tasks

    async def get_tasks_by_id(self, id: str):
        tasks = []
        r = csv.DictReader(open("tasks.csv", "r"))
        for row in r:
            if row['member'] == id:
                tasks.append((row['task'], row['due']))
        return tasks

    async def add(self, member, task: str, due: str, channel: str, message_id: str, dictt: dict):
        r = csv.DictReader(open("tasks.csv", "r"))
        rows = [row for row in r]
        rows.append({'member': member.id, 'task': task, 'due': due, "channel": channel, "message_id": message_id,
                     'dict': str(dictt)})
        w = csv.DictWriter(open("tasks.csv", 'w', newline=''), fieldnames=self.p)
        w.writeheader()
        for row in rows:
            w.writerow(row)
        return

    def get_dict(self):
        dicts = []
        r = csv.DictReader(open("tasks.csv", "r"))
        for row in r:
            dictt = {}
            dictt = row['dict']
            dicts.append(dictt)
        return dicts

    async def delete(self, message_id):
        dictt = {}
        rows = []
        r = csv.DictReader(open("tasks.csv", "r"))
        for row in r:
            if not row["message_id"] == str(message_id):
                rows.append(row)
            else:
                dictt = row['dict']

        w = csv.DictWriter(open("tasks.csv", 'w', newline=''), fieldnames=self.p)
        w.writeheader()
        for row in rows:
            w.writerow(row)
        return dictt

    def write_task_board_info(self, guild_id, embed_id, embed_channel):
        r = csv.DictReader(open("constants.csv", "r"))
        rows = [row for row in r]
        rows.append({'guild_id': guild_id, 'embed_id': embed_id, 'embed_channel': embed_channel})
        w = csv.DictWriter(open("constants.csv", 'w', newline=''), fieldnames=self.constants_p)
        w.writeheader()
        for row in rows:
            w.writerow(row)
        return

    def get_task_board_info_via_guild(self, guild_id):
        r = csv.DictReader(open("constants.csv", "r"))
        for row in r:
            if row['guild_id'] == str(guild_id):
                return int(row['embed_channel'])


