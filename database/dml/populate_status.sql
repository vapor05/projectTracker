INSERT INTO status (status_code, description)
    VALUES ('Proposed', 'This item as been proposed but is not completely planned out and not ready to start'),
        ('Requirement Gathering', 'The items requirements and goals are still being researched and is not ready to start'),
        ('To Do', 'All requirements and goals for this item have been gathered and the item is ready to start but has not been started'),
        ('In Progress', 'This item is actively being worked on'),
        ('Complete', 'This item has been finished and is not being worked on but the item could be worked on more in the future'),
        ('Closed', 'All work has been completed on this item and no more work will be done on this item'),
        ('Wont Do', 'This item will not be worked on'),
        ('Rejected', 'This item will not be worked on'),
        ('Incomplete', 'This item could not be finished');
