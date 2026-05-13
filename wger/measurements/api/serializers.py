# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

# Standard Library
from decimal import Decimal

# Third Party
from rest_framework import serializers

# wger
from wger.measurements.models import (
    Category,
    Measurement,
    CategoryGroup
)


class UnitSerializer(serializers.ModelSerializer):
    """
    Measurement unit serializer
    """
    group_name = serializers.CharField(write_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'unit', 'group_name')
    
    # Creates category group
    def create(self, data):
        group_name = data.pop('group_name', None)
        group, created = CategoryGroup.objects.get_or_create(name=group_name)
        data['group'] = group
        return super().create(data)


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Measurement serializer
    """

    # Manually set the serializer to set the coerce_to_string option
    value = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        min_value=Decimal(0.0),
        max_value=Decimal(5000.0),
        coerce_to_string=False,
    )

    class Meta:
        model = Measurement
        fields = (
            'id',
            'category',
            'date',
            'value',
            'notes',
        )

class CategoryGroupSerializer(serializers.ModelSerializer):
    """
    Category Group Serializer
    """
    class Meta:
        model = CategoryGroup
        fields = ('id', 'name')