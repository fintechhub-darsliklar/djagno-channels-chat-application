



def queryset_to_dict(queryset):

    data = []
    for q in queryset:
        data.append({
            "id": q.id,
            "first_name": q.first_name,
            "last_name": q.last_name,
            "username": q.username,
            "is_online": q.is_active
            # "avatar": q.avatar,
        })
    return data



