
Checking results of various mistakes.

Attempt to create existing repository fails:

  $ hg bb_create mercurial-bitbucketize
  Creating BitBucket repo Mekk/mercurial-bitbucketize
  
  Failed to create BitBucket repository: Repository with this Slug and Owner already exists.
  [1]

Status in case repo does not exist:

  $ hg bb_status utst-non-existing 
  Checking status of BitBucket repo utst-non-existing belonging to Mekk
  
  Repository Mekk/utst-non-existing does not exist on BitBucket
  [1]

Modify non-existing repo:

  $ hg bb_modify utstjustnonexisting --public
  
  Repository Mekk/utstjustnonexisting does not exist on BitBucket
  [1]

Delete non-existing repo:

  $ hg bb_delete utstjustnonexisting
  
  Repository Mekk/utstjustnonexisting does not exist on BitBucket
  [1]

