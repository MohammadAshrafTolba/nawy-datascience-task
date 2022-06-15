# nawy-datascience-task

## Endpoints

- route : /classify_lead
- method : POST
- header : NA
- body : 
```python
{
    'lead_info': {
        'lead_mobile_network': ..., 
        'month': ...,	
        'year': ..., 
        'method_of_contact': ..., 
        'lead_source': ..., 
        'low_qualified': ...
    }
}
```

## Classifier Info

- Type: RandomForrestClassifier
- Reason: Less bias to class imbalance
- Final Recall: 0.07

## For Deployment

### BUILD

```
sudo docker build -t leads_classifier .
```

### RUN

```
sudo docker run -p 3000:3000 -d --name leads_classifier leads_classifier:latest
```
