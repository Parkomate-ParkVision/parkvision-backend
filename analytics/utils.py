from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from django.db.models import QuerySet
import pandas as pd

class KMeansClusterer:
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters)
        self.scaler = StandardScaler()
        self.labels = None
        self.cluster_centers = None
        self.inertia = None
        self.silhouette_score = None

    def fit(self, X):
        X = self.scaler.fit_transform(X)
        self.model.fit(X)
        self.labels = self.model.labels_
        self.cluster_centers = self.model.cluster_centers_
        self.inertia = self.model.inertia_
        self.silhouette_score = silhouette_score(X, self.labels)

    def predict(self, X):
        X = self.scaler.transform(X)
        return self.model.predict(X)

    def fit_predict(self, X):
        self.fit(X)
        return self.predict(X)
    
    def get_cluster_centers(self):
        return self.cluster_centers
    
    def get_labels(self):
        return self.labels
    
    def get_inertia(self):
        return self.inertia
    
    def get_silhouette_score(self):
        return self.silhouette_score
    
    def get_n_clusters(self):
        return self.n_clusters
    
    def get_model(self):
        return self.model
    
    def get_scaler(self):
        return self.scaler
    
    def set_n_clusters(self, n_clusters):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters)

class MeanShiftClusterer:
    def __init__(self, bandwidth=None):
        self.bandwidth = bandwidth
        self.model = MeanShift(bandwidth=bandwidth)
        self.scaler = StandardScaler()
        self.labels = None
        self.cluster_centers = None
        self.inertia = None
        self.silhouette_score = None

    def fit(self, X):
        X = self.scaler.fit_transform(X)
        self.model.fit(X)
        self.labels = self.model.labels_
        self.cluster_centers = self.model.cluster_centers_
        self.inertia = self.model.inertia_
        self.silhouette_score = silhouette_score(X, self.labels)

    def predict(self, X):
        X = self.scaler.transform(X)
        return self.model.predict(X)

    def fit_predict(self, X):
        self.fit(X)
        return self.predict(X)
    
    def get_cluster_centers(self):
        return self.cluster_centers
    
    def get_labels(self):
        return self.labels
    
    def get_inertia(self):
        return self.inertia
    
    def get_silhouette_score(self):
        return self.silhouette_score
    
    def get_bandwidth(self):
        return self.bandwidth
    
    def get_model(self):
        return self.model
    
    def get_scaler(self):
        return self.scaler
    
    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.model = MeanShift(bandwidth=bandwidth)

class DataLoader:
    def __init__(self, vehicle_details_queryset: QuerySet, per_hour_vehicle_count_queryset: QuerySet):
        self.vehicle_details_queryset = vehicle_details_queryset
        self.per_hour_vehicle_count_queryset = per_hour_vehicle_count_queryset
        self.vehicle_details_dataframe = None
        self.per_hour_vehicle_count_dataframe = None

    def load_vehicle_details(self):
        self.vehicle_details_dataframe = pd.DataFrame.from_records(self.vehicle_details_queryset.values())
        return self.vehicle_details_dataframe
    
    def load_per_hour_vehicle_count(self):
        self.per_hour_vehicle_count_dataframe = pd.DataFrame.from_records(self.per_hour_vehicle_count_queryset.values())
        return self.per_hour_vehicle_count_dataframe
    
    def get_vehicle_details_dataframe(self):
        return self.vehicle_details_dataframe
    
    def get_per_hour_vehicle_count_dataframe(self):
        return self.per_hour_vehicle_count_dataframe
    
    def get_vehicle_details_queryset(self):
        return self.vehicle_details_queryset
    
    def get_per_hour_vehicle_count_queryset(self):
        return self.per_hour_vehicle_count_queryset
    
    def set_vehicle_details_queryset(self, vehicle_details_queryset):
        self.vehicle_details_queryset = vehicle_details_queryset

    def set_per_hour_vehicle_count_queryset(self, per_hour_vehicle_count_queryset):
        self.per_hour_vehicle_count_queryset = per_hour_vehicle_count_queryset

class DataPreprocessor:
    def __init__(self, vehicle_details_dataframe: pd.DataFrame, per_hour_vehicle_count_dataframe: pd.DataFrame):
        self.vehicle_details_dataframe = vehicle_details_dataframe
        self.per_hour_vehicle_count_dataframe = per_hour_vehicle_count_dataframe
        self.vehicle_details_dataframe = self.vehicle_details_dataframe.dropna()
        self.per_hour_vehicle_count_dataframe = self.per_hour_vehicle_count_dataframe.dropna()
        self.vehicle_details_dataframe = self.vehicle_details_dataframe.drop_duplicates()
        self.per_hour_vehicle_count_dataframe = self.per_hour_vehicle_count_dataframe.drop_duplicates()
        self.vehicle_details_dataframe = self.vehicle_details_dataframe.reset_index(drop=True)
        self.per_hour_vehicle_count_dataframe = self.per_hour_vehicle_count_dataframe.reset_index(drop=True)
        self.vehicle_details_dataframe['registration_date'] = pd.to_datetime(self.vehicle_details_dataframe['registration_date'])
        self.vehicle_details_dataframe['puc_valid_upto'] = pd.to_datetime(self.vehicle_details_dataframe['puc_valid_upto'])
        self.vehicle_details_dataframe['permit_validity_from'] = pd.to_datetime(self.vehicle_details_dataframe['permit_validity_from'])
        self.vehicle_details_dataframe['permit_validity_to'] = pd.to_datetime(self.vehicle_details_dataframe['permit_validity_to'])
        self.vehicle_details_dataframe['created_at'] = pd.to_datetime(self.vehicle_details_dataframe['created_at'])
        self.per_hour_vehicle_count_dataframe['created_at'] = pd.to_datetime(self.per_hour_vehicle_count_dataframe['created_at'])
        self.per_hour_vehicle_count_dataframe['organization_id'] = self.per_hour_vehicle_count_dataframe['organization_id'].astype(str)
        self.per_hour_vehicle_count_dataframe['vehicle_count'] = self.per_hour_vehicle_count_dataframe['vehicle_count'].astype(int)
        self.per_hour_vehicle_count_dataframe['vehicle_type'] = self.per_hour_vehicle_count_dataframe['vehicle_type'].astype(str)
        self.per_hour_vehicle_count_dataframe['created_at'] = pd.to_datetime(self.per_hour_vehicle_count_dataframe['created_at'])
        self.per_hour_vehicle_count_dataframe['created_at'] = self.per_hour_vehicle_count_dataframe['created_at'].dt.tz_localize(None)
        self.vehicle_details_dataframe['registration_date'] = self.vehicle_details_dataframe['registration_date'].dt.tz_localize(None)
        self.vehicle_details_dataframe['puc_valid_upto'] = self.vehicle_details_dataframe['puc_valid_upto'].dt.tz_localize(None)
        self.vehicle_details_dataframe['permit_validity_from'] = self.vehicle_details_dataframe['permit_validity_from'].dt.tz_localize(None)

    def preprocess_vehicle_details_dataframe(self):
        self.vehicle_details_dataframe = self.vehicle_details_dataframe.drop(['id', 'vehicle_id', 'vehicle_type', 'owner_address', 'permit_no', 'permit_type', 'registration_number', 'insurance_policy_no', 'owner_mobile_no', 'insurance_name', 'permanent_address', 'owner_name', 'manufacturer', 'manufacturer_model', 'fuel_type', 'seating_capacity', 'registered_place', 'father_name', 'current_address'], axis=1)
        return self.vehicle_details_dataframe
    
    def preprocess_per_hour_vehicle_count_dataframe(self):
        self.per_hour_vehicle_count_dataframe = self.per_hour_vehicle_count_dataframe.drop(['id'], axis=1)
        return self.per_hour_vehicle_count_dataframe
    
    def get_vehicle_details_dataframe(self):
        return self.vehicle_details_dataframe
    
    def get_per_hour_vehicle_count_dataframe(self):
        return self.per_hour_vehicle_count_dataframe
    
    def set_vehicle_details_dataframe(self, vehicle_details_dataframe):
        self.vehicle_details_dataframe = vehicle_details_dataframe

    def set_per_hour_vehicle_count_dataframe(self, per_hour_vehicle_count_dataframe):
        self.per_hour_vehicle_count_dataframe = per_hour_vehicle_count_dataframe

class DataAnalyzer:
    def __init__(self, vehicle_details_queryset: QuerySet, per_hour_vehicle_count_queryset: QuerySet):
        self.data_loader = DataLoader(vehicle_details_queryset, per_hour_vehicle_count_queryset)
        self.vehicle_details_dataframe = None
        self.per_hour_vehicle_count_dataframe = None
        self.data_preprocessor = None
        self.vehicle_details_dataframe = None
        self.per_hour_vehicle_count_dataframe = None
        self.knn_classifier = None
        self.kmeans_clusterer = None
        self.mean_shift_clusterer = None
        self.vehicle_type = None
        self.vehicle_type_prediction_accuracy = None
        self.vehicle_type_prediction_confidence = None
        self.vehicle_type_prediction_confidence_threshold = 0.5
        self.vehicle_type_prediction_accuracy_threshold = 0.5
        self.vehicle_type_prediction_confidence_threshold = 0.5
        self.vehicle_type_prediction_accuracy_threshold = 0.5

    def load_data(self):
        self.vehicle_details_dataframe = self.data_loader.load_vehicle_details()
        self.per_hour_vehicle_count_dataframe = self.data_loader.load_per_hour_vehicle_count()
        return self.vehicle_details_dataframe, self.per_hour_vehicle_count_dataframe
    
    def preprocess_data(self):
        self.data_preprocessor = DataPreprocessor(self.vehicle_details_dataframe, self.per_hour_vehicle_count_dataframe)
        self.vehicle_details_dataframe = self.data_preprocessor.preprocess_vehicle_details_dataframe()
        self.per_hour_vehicle_count_dataframe = self.data_preprocessor.preprocess_per_hour_vehicle_count_dataframe()
        return self.vehicle_details_dataframe, self.per_hour_vehicle_count_dataframe
    
    def analyze_data(self):
        self.knn_classifier = KNeighborsClassifier(n_neighbors=3)
        self.kmeans_clusterer = KMeansClusterer(n_clusters=3)
        self.mean_shift_clusterer = MeanShiftClusterer()
        self.knn_classifier.fit(self.vehicle_details_dataframe[['registration_date', 'puc_valid_upto', 'permit_validity_from', 'permit_validity_to', 'created_at']])
        self.kmeans_clusterer.fit(self.per_hour_vehicle_count_dataframe[['organization_id', 'vehicle_count']])
        self.mean_shift_clusterer.fit(self.per_hour_vehicle_count_dataframe[['organization_id', 'vehicle_count']])
        self.vehicle_type = self.knn_classifier.predict(self.vehicle_details_dataframe[['registration_date', 'puc_valid_upto', 'permit_validity_from', 'permit_validity_to', 'created_at']])
        self.vehicle_type_prediction_accuracy = self.knn_classifier.score(self.vehicle_details_dataframe[['registration_date', 'puc_valid_upto', 'permit_validity_from', 'permit_validity_to', 'created_at']], self.vehicle_type)
        self.vehicle_type_prediction_confidence = self.knn_classifier.predict_proba(self.vehicle_details_dataframe[['registration_date', 'puc_valid_upto', 'permit_validity_from', 'permit_validity_to', 'created_at']])
        return self.vehicle_type, self.vehicle_type_prediction_accuracy, self.vehicle_type_prediction_confidence
    
    def get_vehicle_details_dataframe(self):
        return self.vehicle_details_dataframe
    
    def get_per_hour_vehicle_count_dataframe(self):
        return self.per_hour_vehicle_count_dataframe
    
    def get_data_loader(self):
        return self.data_loader
    
    def get_data_preprocessor(self):
        return self.data_preprocessor
    
    def get_knn_classifier(self):
        return self.knn_classifier
    
    def get_kmeans_clusterer(self):
        return self.kmeans_clusterer
    
    def get_mean_shift_clusterer(self):
        return self.mean_shift_clusterer
    
    def get_vehicle_type(self):
        return self.vehicle_type
    
    def get_vehicle_type_prediction_accuracy(self):
        return self.vehicle_type_prediction_accuracy
    
    def get_vehicle_type_prediction_confidence(self):
        return self.vehicle_type_prediction_confidence
    
    def get_vehicle_type_prediction_confidence_threshold(self):
        return self.vehicle_type_prediction_confidence_threshold
    
    def get_vehicle_type_prediction_accuracy_threshold(self):
        return self.vehicle_type_prediction_accuracy_threshold
    
    def set_vehicle_details_dataframe(self, vehicle_details_dataframe):
        self.vehicle_details_dataframe = vehicle_details_dataframe

    def set_per_hour_vehicle_count_dataframe(self, per_hour_vehicle_count_dataframe):
        self.per_hour_vehicle_count_dataframe = per_hour_vehicle_count_dataframe

    def set_data_loader(self, data_loader):
        self.data_loader = data_loader

    def set_data_preprocessor(self, data_preprocessor):
        self.data_preprocessor = data_preprocessor

    def set_knn_classifier(self, knn_classifier):
        self.knn_classifier = knn_classifier

    def set_kmeans_clusterer(self, kmeans_clusterer):
        self.kmeans_clusterer = kmeans_clusterer

    def set_mean_shift_clusterer(self, mean_shift_clusterer):
        self.mean_shift_clusterer = mean_shift_clusterer

    def set_vehicle_type(self, vehicle_type):
        self.vehicle_type = vehicle_type

    def set_vehicle_type_prediction_accuracy(self, vehicle_type_prediction_accuracy):
        self.vehicle_type_prediction_accuracy = vehicle_type_prediction_accuracy

    def set_vehicle_type_prediction_confidence(self, vehicle_type_prediction_confidence):
        self.vehicle_type_prediction_confidence = vehicle_type_prediction_confidence

    def set_vehicle_type_prediction_confidence_threshold(self, vehicle_type_prediction_confidence_threshold):
        self.vehicle_type_prediction_confidence_threshold = vehicle_type_prediction_confidence_threshold

    def set_vehicle_type_prediction_accuracy_threshold(self, vehicle_type_prediction_accuracy_threshold):
        self.vehicle_type_prediction_accuracy_threshold = vehicle_type_prediction_accuracy_threshold