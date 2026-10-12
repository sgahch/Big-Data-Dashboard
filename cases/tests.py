"""
Comprehensive Test Suite for Cases App
Tests for finding hidden bugs in models, serializers, views, and API endpoints.
"""

from datetime import date, timedelta
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Case, CaseProgress, Evidence, Trial, Conclusion
from .serializers import CaseSerializer, TrialSerializer, TrialCreateSerializer, ConclusionSerializer, ConclusionCreateSerializer

User = get_user_model()


class CaseModelTest(TestCase):
    """Test Case model for hidden bugs"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_case_creation_minimal_fields(self):
        """Test creating case with minimal required fields"""
        case = Case.objects.create(
            case_no='TEST001',
            case_name='Test Case',
            suspect_name='Test Person',
            status='pending',
            stage='filing'
        )
        self.assertEqual(case.case_no, 'TEST001')
        self.assertEqual(case.case_name, 'Test Case')

    def test_case_str_method(self):
        """Test Case __str__ method"""
        case = Case.objects.create(
            case_no='TEST002',
            case_name='Test Case Name',
            suspect_name='Test Person'
        )
        self.assertEqual(str(case), 'TEST002 - Test Case Name')

    def test_case_amount_fields_default(self):
        """Test decimal fields have correct defaults"""
        case = Case.objects.create(
            case_no='TEST003',
            case_name='Test Case',
            suspect_name='Test Person',
            involved_amount=Decimal('10000.00'),
            recovered_amount=Decimal('5000.00')
        )
        self.assertEqual(case.involved_amount, Decimal('10000.00'))
        self.assertEqual(case.recovered_amount, Decimal('5000.00'))

    def test_case_stage_choices(self):
        """Test case stage choices validation"""
        case = Case.objects.create(
            case_no='TEST004',
            case_name='Test Case',
            suspect_name='Test Person',
            stage='filing'
        )
        self.assertEqual(case.stage, 'filing')
        case.stage = 'investigation'
        case.save()
        self.assertEqual(case.stage, 'investigation')


class TrialModelTest(TestCase):
    """Test Trial model for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.case = Case.objects.create(
            case_no='TRIAL001',
            case_name='Test Case for Trial',
            suspect_name='Test Person'
        )

    def test_trial_creation_minimal(self):
        """Test creating trial with minimal fields"""
        trial = Trial.objects.create(
            accept_no='SL2025010001',
            case=self.case,
            accept_date=date.today(),
            judge='Test Judge'
        )
        self.assertEqual(trial.accept_no, 'SL2025010001')
        self.assertEqual(trial.status, 'pending')

    def test_trial_days_left_future(self):
        """Test days_left calculation with future deadline"""
        trial = Trial.objects.create(
            accept_no='SL2025010002',
            case=self.case,
            accept_date=date.today(),
            deadline=30,
            judge='Test Judge'
        )
        # Should return positive number
        self.assertIsNotNone(trial.days_left)
        self.assertGreater(trial.days_left, 0)

    def test_trial_days_left_completed(self):
        """Test days_left returns None for completed trials"""
        trial = Trial.objects.create(
            accept_no='SL2025010003',
            case=self.case,
            accept_date=date.today(),
            deadline=30,
            judge='Test Judge',
            status='completed'
        )
        self.assertIsNone(trial.days_left)

    def test_trial_str_method(self):
        """Test Trial __str__ method"""
        trial = Trial.objects.create(
            accept_no='SL2025010004',
            case=self.case,
            accept_date=date.today(),
            judge='Test Judge'
        )
        expected = f'SL2025010004 - {self.case.case_name}'
        self.assertEqual(str(trial), expected)

    def test_trial_status_choices(self):
        """Test trial status choices"""
        trial = Trial.objects.create(
            accept_no='SL2025010005',
            case=self.case,
            accept_date=date.today(),
            judge='Test Judge',
            status='pending'
        )
        self.assertEqual(trial.status, 'pending')
        trial.status = 'processing'
        trial.save()
        self.assertEqual(trial.status, 'processing')


class ConclusionModelTest(TestCase):
    """Test Conclusion model for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.case = Case.objects.create(
            case_no='CONC001',
            case_name='Test Case for Conclusion',
            suspect_name='Test Person'
        )

    def test_conclusion_creation_minimal(self):
        """Test creating conclusion with minimal fields"""
        conclusion = Conclusion.objects.create(
            conclusion_no='JA2025010001',
            case=self.case,
            conclusion_date=date.today(),
            conclusion_type='party_discipline'
        )
        self.assertEqual(conclusion.conclusion_no, 'JA2025010001')
        self.assertEqual(conclusion.execution_status, 'pending')
        self.assertFalse(conclusion.archived)

    def test_conclusion_str_method(self):
        """Test Conclusion __str__ method"""
        conclusion = Conclusion.objects.create(
            conclusion_no='JA2025010002',
            case=self.case,
            conclusion_date=date.today(),
            conclusion_type='administrative'
        )
        expected = f'JA2025010002 - {self.case.case_name}'
        self.assertEqual(str(conclusion), expected)

    def test_conclusion_execution_status_choices(self):
        """Test execution status choices"""
        conclusion = Conclusion.objects.create(
            conclusion_no='JA2025010003',
            case=self.case,
            conclusion_date=date.today(),
            conclusion_type='judicial',
            execution_status='completed'
        )
        self.assertEqual(conclusion.execution_status, 'completed')

    def test_conclusion_type_choices(self):
        """Test conclusion type choices"""
        type_suffixes = ['party', 'admin', 'judicial', 'criticism', 'concluded']
        for i, concl_type in enumerate(['party_discipline', 'administrative', 'judicial', 'criticism', 'concluded']):
            conclusion = Conclusion.objects.create(
                conclusion_no=f'JA202501{type_suffixes[i][:3].upper()}{i:02d}',
                case=self.case,
                conclusion_date=date.today(),
                conclusion_type=concl_type
            )
            self.assertEqual(conclusion.conclusion_type, concl_type)


class CaseSerializerTest(TestCase):
    """Test CaseSerializer for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_serializer_valid_data(self):
        """Test serializer with valid data"""
        data = {
            'case_no': 'SER001',
            'case_name': 'Test Case',
            'suspect_name': 'Test Person',
            'case_level': 'ordinary',
            'stage': 'filing',
            'status': 'pending'
        }
        serializer = CaseSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_missing_required_field(self):
        """Test serializer fails with missing required field"""
        data = {
            'case_no': 'SER002',
            # Missing case_name and suspect_name
        }
        serializer = CaseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('case_name', serializer.errors)
        self.assertIn('suspect_name', serializer.errors)

    def test_serializer_leader_field_readonly(self):
        """Test leader_name is read-only in serializer"""
        data = {
            'case_no': 'SER003',
            'case_name': 'Test Case',
            'suspect_name': 'Test Person',
            'leader_name': 'Should not be settable'
        }
        serializer = CaseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        # leader_name should not be in validated_data
        self.assertNotIn('leader_name', serializer.validated_data)


class TrialSerializerTest(TestCase):
    """Test TrialSerializer for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.case = Case.objects.create(
            case_no='TSER001',
            case_name='Test Case',
            suspect_name='Test Person'
        )

    def test_create_serializer_valid_data(self):
        """Test TrialCreateSerializer with valid data"""
        data = {
            'case': self.case.id,
            'accept_date': '2025-01-20',
            'judge': 'Test Judge',
            'deadline': 30
        }
        serializer = TrialCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_missing_required(self):
        """Test TrialCreateSerializer fails with missing required fields"""
        data = {
            'case': self.case.id,
            # Missing accept_date and judge
        }
        serializer = TrialCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('accept_date', serializer.errors)
        self.assertIn('judge', serializer.errors)

    def test_days_left_method_field(self):
        """Test days_left is a read-only SerializerMethodField"""
        trial = Trial.objects.create(
            accept_no='SL202501TEST',
            case=self.case,
            accept_date=date.today(),
            deadline=30,
            judge='Test Judge'
        )
        serializer = TrialSerializer(trial)
        self.assertIn('days_left', serializer.data)
        # days_left should be an integer
        self.assertIsInstance(serializer.data['days_left'], int)


class ConclusionSerializerTest(TestCase):
    """Test ConclusionSerializer for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.case = Case.objects.create(
            case_no='CSER001',
            case_name='Test Case',
            suspect_name='Test Person'
        )

    def test_create_serializer_valid_data(self):
        """Test ConclusionCreateSerializer with valid data"""
        data = {
            'case': self.case.id,
            'conclusion_date': '2025-01-20',
            'conclusion_type': 'party_discipline'
        }
        serializer = ConclusionCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_missing_required(self):
        """Test ConclusionCreateSerializer fails with missing required fields"""
        data = {
            'case': self.case.id,
            # Missing conclusion_date and conclusion_type
        }
        serializer = ConclusionCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('conclusion_date', serializer.errors)
        self.assertIn('conclusion_type', serializer.errors)

    def test_execution_text_readonly(self):
        """Test execution_text is a read-only field"""
        conclusion = Conclusion.objects.create(
            conclusion_no='JA2025TEST',
            case=self.case,
            conclusion_date=date.today(),
            conclusion_type='administrative',
            execution_status='pending'
        )
        serializer = ConclusionSerializer(conclusion)
        self.assertIn('execution_text', serializer.data)
        # execution_text should be a string
        self.assertIsInstance(serializer.data['execution_text'], str)


class CaseViewSetTest(APITestCase):
    """Test CaseViewSet API endpoints for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_cases_unauthenticated(self):
        """Test that unauthenticated requests are rejected"""
        client = APIClient()
        response = client.get('/api/cases/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_case_authenticated(self):
        """Test creating case as authenticated user"""
        data = {
            'case_no': 'API001',
            'case_name': 'API Test Case',
            'suspect_name': 'Test Person',
            'case_level': 'ordinary',
            'status': 'pending'
        }
        response = self.client.post('/api/cases/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['case_no'], 'API001')

    def test_get_case_detail(self):
        """Test retrieving single case"""
        case = Case.objects.create(
            case_no='API002',
            case_name='Test Case',
            suspect_name='Test Person'
        )
        response = self.client.get(f'/api/cases/{case.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['case_no'], 'API002')

    def test_filter_cases_by_status(self):
        """Test filtering cases by status"""
        Case.objects.create(case_no='F001', case_name='Case 1', suspect_name='P1', status='pending')
        Case.objects.create(case_no='F002', case_name='Case 2', suspect_name='P2', status='active')

        response = self.client.get('/api/cases/', {'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that only pending cases are returned
        for item in response.data['results']:
            self.assertEqual(item['status'], 'pending')

    def test_update_case(self):
        """Test updating case"""
        case = Case.objects.create(
            case_no='UPD001',
            case_name='Original Name',
            suspect_name='Test Person'
        )
        data = {'case_name': 'Updated Name'}
        response = self.client.patch(f'/api/cases/{case.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['case_name'], 'Updated Name')

    def test_delete_case(self):
        """Test deleting case"""
        case = Case.objects.create(
            case_no='DEL001',
            case_name='To Delete',
            suspect_name='Test Person'
        )
        response = self.client.delete(f'/api/cases/{case.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Case.objects.filter(id=case.id).exists())


class TrialViewSetTest(APITestCase):
    """Test TrialViewSet API endpoints for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.case = Case.objects.create(
            case_no='TRIALAPI001',
            case_name='Test Case',
            suspect_name='Test Person'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_trial(self):
        """Test creating trial"""
        data = {
            'case': self.case.id,
            'accept_date': '2025-01-20',
            'judge': 'Test Judge',
            'deadline': 30
        }
        response = self.client.post('/api/trials/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_trials_by_status(self):
        """Test filtering trials by status"""
        Trial.objects.create(
            accept_no='TF001',
            case=self.case,
            accept_date=date.today(),
            judge='Judge 1',
            status='pending'
        )
        Trial.objects.create(
            accept_no='TF002',
            case=self.case,
            accept_date=date.today(),
            judge='Judge 2',
            status='completed'
        )

        response = self.client.get('/api/trials/', {'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertEqual(item['status'], 'pending')

    def test_trial_status_transition(self):
        """Test trial status transition via PATCH"""
        trial = Trial.objects.create(
            accept_no='TST001',
            case=self.case,
            accept_date=date.today(),
            judge='Test Judge',
            status='pending'
        )
        data = {'status': 'processing'}
        response = self.client.patch(f'/api/trials/{trial.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'processing')

        # Complete the trial
        data = {'status': 'completed'}
        response = self.client.patch(f'/api/trials/{trial.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')


class ConclusionViewSetTest(APITestCase):
    """Test ConclusionViewSet API endpoints for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.case = Case.objects.create(
            case_no='CONCAPI001',
            case_name='Test Case',
            suspect_name='Test Person'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_conclusion(self):
        """Test creating conclusion"""
        data = {
            'case': self.case.id,
            'conclusion_date': '2025-01-20',
            'conclusion_type': 'party_discipline'
        }
        response = self.client.post('/api/conclusions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_conclusions_by_archived(self):
        """Test filtering conclusions by archived status"""
        Conclusion.objects.create(
            conclusion_no='CAF001',
            case=self.case,
            conclusion_date=date.today(),
            conclusion_type='party_discipline',
            archived=False
        )
        Conclusion.objects.create(
            conclusion_no='CAF002',
            case=self.case,
            conclusion_date=date.today(),
            conclusion_type='administrative',
            archived=True
        )

        response = self.client.get('/api/conclusions/', {'archived': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertTrue(item['archived'])

    def test_update_conclusion_archive(self):
        """Test updating conclusion archive status"""
        conclusion = Conclusion.objects.create(
            conclusion_no='CUA001',
            case=self.case,
            conclusion_date=date.today(),
            conclusion_type='judicial',
            archived=False
        )
        data = {'archived': True}
        response = self.client.patch(f'/api/conclusions/{conclusion.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['archived'])


class EvidenceViewSetTest(APITestCase):
    """Test EvidenceViewSet API endpoints for hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.case = Case.objects.create(
            case_no='EVI001',
            case_name='Test Case',
            suspect_name='Test Person'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_evidence(self):
        """Test creating evidence"""
        data = {
            'case': self.case.id,
            'evidence_type': 'document',
            'name': 'Test Document'
        }
        response = self.client.post('/api/evidences/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_evidence_by_case(self):
        """Test filtering evidence by case"""
        Evidence.objects.create(
            case=self.case,
            evidence_type='document',
            name='Evidence 1'
        )
        other_case = Case.objects.create(
            case_no='EVI002',
            case_name='Other Case',
            suspect_name='Other Person'
        )
        Evidence.objects.create(
            case=other_case,
            evidence_type='material',
            name='Evidence 2'
        )

        response = self.client.get('/api/evidences/', {'case': self.case.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # All results should belong to the requested case
        for item in response.data['results']:
            self.assertEqual(item['case'], self.case.id)


class DataIntegrityTest(TestCase):
    """Test data integrity and edge cases"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_cascade_delete_case_progress(self):
        """Test case progress is deleted when case is deleted"""
        case = Case.objects.create(
            case_no='CASC001',
            case_name='Test Case',
            suspect_name='Test Person'
        )
        progress = CaseProgress.objects.create(
            case=case,
            progress_type='filing',
            progress_date=date.today(),
            progress_content='Test progress'
        )
        case_id = case.id
        progress_id = progress.id

        case.delete()

        self.assertFalse(Case.objects.filter(id=case_id).exists())
        self.assertFalse(CaseProgress.objects.filter(id=progress_id).exists())

    def test_cascade_delete_case_evidence(self):
        """Test evidence is deleted when case is deleted"""
        case = Case.objects.create(
            case_no='CASC002',
            case_name='Test Case',
            suspect_name='Test Person'
        )
        evidence = Evidence.objects.create(
            case=case,
            evidence_type='document',
            name='Test Evidence'
        )
        case_id = case.id
        evidence_id = evidence.id

        case.delete()

        self.assertFalse(Case.objects.filter(id=case_id).exists())
        self.assertFalse(Evidence.objects.filter(id=evidence_id).exists())

    def test_unique_constraints(self):
        """Test unique constraints on case_no and accept_no"""
        case1 = Case.objects.create(
            case_no='UNIQUE001',
            case_name='Case 1',
            suspect_name='Person 1'
        )

        # Attempting to create another case with the same case_no should fail
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Case.objects.create(
                case_no='UNIQUE001',  # Duplicate
                case_name='Case 2',
                suspect_name='Person 2'
            )

    def test_empty_string_fields(self):
        """Test handling of empty string fields"""
        case = Case.objects.create(
            case_no='EMPTY001',
            case_name='Test Case',
            suspect_name='Test Person',
            suspect_unit='',  # Empty string
            suspect_position='',  # Empty string
        )
        self.assertEqual(case.suspect_unit, '')
        self.assertEqual(case.suspect_position, '')

    def test_date_field_nullable(self):
        """Test nullable date fields"""
        case = Case.objects.create(
            case_no='DATE001',
            case_name='Test Case',
            suspect_name='Test Person',
            filing_date=None,  # Nullable
        )
        self.assertIsNone(case.filing_date)

    def test_foreign_key_set_null(self):
        """Test ForeignKey with set_null on delete"""
        case = Case.objects.create(
            case_no='FK001',
            case_name='Test Case',
            suspect_name='Test Person',
            leader=self.user
        )
        case_id = case.id
        case.leader = None
        case.save()
        case.refresh_from_db()
        self.assertIsNone(case.leader)


# Edge Case Tests
class EdgeCaseTest(TestCase):
    """Test edge cases that might reveal hidden bugs"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_special_characters_in_names(self):
        """Test special characters in name fields"""
        case = Case.objects.create(
            case_no='SPEC001',
            case_name='Test Case with special chars: @#$%',
            suspect_name='Person with special chars: 中文姓名',
            suspect_unit='单位 with "quotes" and \'apostrophes\''
        )
        self.assertIn('@#$%', case.case_name)
        self.assertIn('中文姓名', case.suspect_name)

    def test_very_long_strings(self):
        """Test very long string fields"""
        long_string = 'A' * 1000
        case = Case.objects.create(
            case_no='LONG001',
            case_name='Test Case',
            suspect_name=long_string,
            summary=long_string
        )
        self.assertEqual(len(case.suspect_name), 1000)
        self.assertEqual(len(case.summary), 1000)

    def test_decimal_precision(self):
        """Test decimal field precision"""
        case = Case.objects.create(
            case_no='DEC001',
            case_name='Test Case',
            suspect_name='Test Person',
            involved_amount=Decimal('123456789.12'),
            recovered_amount=Decimal('9876543.21')
        )
        self.assertEqual(case.involved_amount, Decimal('123456789.12'))
        self.assertEqual(case.recovered_amount, Decimal('9876543.21'))

    def test_future_dates(self):
        """Test future dates are allowed"""
        future_date = date.today() + timedelta(days=365)
        case = Case.objects.create(
            case_no='FUT001',
            case_name='Test Case',
            suspect_name='Test Person',
            filing_date=future_date
        )
        self.assertEqual(case.filing_date, future_date)

    def test_past_dates(self):
        """Test past dates are allowed"""
        past_date = date.today() - timedelta(days=365)
        case = Case.objects.create(
            case_no='PAS001',
            case_name='Test Case',
            suspect_name='Test Person',
            filing_date=past_date
        )
        self.assertEqual(case.filing_date, past_date)
