
class LeaveRequestFilterBackend():
    def filter_queryset(self, request, queryset, view):
        # filter_by = request.query_params.get('filter_by', 'all')
        employee_id = request.query_params.get('employee_id', None)
        office_id = request.query_params.get('office_id', None)
        team = request.query_params.get('team', None)

        if employee_id:
            if employee_id == "null":
                return queryset.none()
            queryset = queryset.filter(employee__id = employee_id)
        elif office_id:
            queryset = queryset.filter(employee__office_id = office_id)
        elif team:
            # queryset = queryset.filter(team_id = team) 
            return queryset.none()
        else :
            return queryset

        return queryset
