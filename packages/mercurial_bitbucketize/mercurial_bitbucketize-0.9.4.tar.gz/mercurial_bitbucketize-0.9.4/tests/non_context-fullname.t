
Some opts create with repo given by full name:

  $ hg bitbucket_create Mekk/utstthird --forks=private --language=c++
  Creating BitBucket repo Mekk/utstthird
  Repository created
  
  Repository: Mekk/utstthird  (scm: hg, size: *.* kB) (glob)
  Access: private   (owner: Mekk)
  Issues: no, wiki: no, forks: private, language: c++
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utstthird
      (ssh)      ssh://hg@bitbucket.org/Mekk/utstthird
  No description
  
  Now `hg push https://bitbucket.org/Mekk/utstthird` to push the code
  Visit https://bitbucket.org/Mekk/utstthird to review details

Checking status:

  $ hg bb_status Mekk/utstthird
  Checking status of BitBucket repo utstthird belonging to Mekk
  
  Repository: Mekk/utstthird  (scm: hg, size: *.* kB) (glob)
  Access: private   (owner: Mekk)
  Issues: no, wiki: no, forks: private, language: c++
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utstthird
      (ssh)      ssh://hg@bitbucket.org/Mekk/utstthird
  No description

Modifying:

  $ hg bb_modify Mekk/utstthird --language=xml --wiki
  Applying BitBucket metadata changes (API v1)
  Changes saved
  
  Repository: Mekk/utstthird  (scm: hg, size: *.* kB) (glob)
  Access: private   (owner: Mekk)
  Issues: no, wiki: yes, forks: private, language: xml
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utstthird
      (ssh)      ssh://hg@bitbucket.org/Mekk/utstthird
  No description

Cleaning up:

  $ hg bb_delete --force Mekk/utstthird
  
  Repository: Mekk/utstthird  (scm: hg, size: *.* kB) (glob)
  Access: private   (owner: Mekk)
  Issues: no, wiki: yes, forks: private, language: xml
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utstthird
      (ssh)      ssh://hg@bitbucket.org/Mekk/utstthird
  No description
  Deleting BitBucket clone Mekk/utstthird
  BitBucket clone deleted


Verifying whether it is missing:

  $ hg bb_status Mekk/utsthird
  Checking status of BitBucket repo utsthird belonging to Mekk
  
  Repository Mekk/utsthird does not exist on BitBucket
  [1]


