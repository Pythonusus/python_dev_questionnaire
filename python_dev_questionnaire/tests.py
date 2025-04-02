from django.urls import reverse_lazy


class TestIndex:
    def test_index(self, client):
        response = client.get(reverse_lazy('index'))
        assert response.status_code == 200
        assert 'index.html' in [t.name for t in response.templates]
