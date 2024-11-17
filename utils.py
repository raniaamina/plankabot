def get_list_name(lists, list_id):
    """
    Cari nama list berdasarkan listId.
    """
    for lst in lists:
        if lst.get("id") == list_id:
            return lst.get("name", "Nama tidak ditemukan")
    return "Nama tidak ditemukan"
