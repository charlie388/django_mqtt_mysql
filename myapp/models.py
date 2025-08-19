from django.db import models

# Create your models here.
class Upload(models.Model):
    # MySQL SERIAL ≈ BIGINT UNSIGNED AUTO_INCREMENT UNIQUE.
    # Django doesn't have an unsigned autoincrement type; BigAutoField is the closest.
    id = models.BigAutoField(primary_key=True)

    device = models.CharField(max_length=48)        # VARCHAR(48) NOT NULL
    upload = models.CharField(max_length=1024)      # VARCHAR(1024) NOT NULL

    # TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    created = models.DateTimeField(auto_now_add=True)

    # TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    # (not declared NOT NULL in your SQL, so we allow NULLs)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "upload"

'''
CREATE TABLE upload (
	id SERIAL,
	device VARCHAR(48) NOT NULL,
	upload VARCHAR(1024) NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (ID)
);
'''